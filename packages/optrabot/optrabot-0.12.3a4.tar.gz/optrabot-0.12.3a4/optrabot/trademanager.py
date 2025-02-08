import asyncio
import json
import pytz
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
from loguru import logger
from optrabot.broker.brokerconnector import BrokerConnector
from optrabot import crud, schemas
from optrabot.optionhelper import OptionHelper
from optrabot.broker.brokerfactory import BrokerFactory
from optrabot.broker.order import Execution, Order, OrderAction, OrderStatus
from optrabot.database import get_db_engine
from optrabot.models import Trade
from optrabot.tradehelper import TradeHelper
from optrabot.tradetemplate.templatefactory import Template
from optrabot.util.singletonmeta import SingletonMeta
from sqlalchemy.orm import Session
from typing import List

class ManagedTrade:
	"""
	ManagedTrade is representing a trade which is currently managed by the TradeManager.
	"""
	def __init__(self, trade: Trade, template: Template, entryOrder: Order, account: str = ''): 
		self.trade = trade
		self.entryOrder = entryOrder
		self.template = template
		self.account = account
		self.takeProfitOrder: Order = None
		self.stopLossOrder: Order = None
		self.status = 'NEW'
		self.realizedPNL = 0.0
		self.transactions = []
		self.expired = False

	def isActive(self) -> bool:
		"""
		Returns True if the trade is active
		"""
		return self.status == 'OPEN'

class TradeManager(metaclass=SingletonMeta):
	"""
	The Trade Manager is a singleton class which is responsible for opening new trades and
	managing existing trades. It is monitoring the open trades and their attachde orders.
	"""
	def __init__(self):
		self._trades: List[ManagedTrade] = []
		self._backgroundScheduler = AsyncIOScheduler()
		self._backgroundScheduler.start()
		self._backgroundScheduler.add_job(self._monitorOpenTrades, 'interval', seconds=5, id='MonitorOpenTrades', misfire_grace_time = None)
		self._backgroundScheduler.add_job(self._performEODTasks, 'cron', hour=16, minute=00, timezone=pytz.timezone('US/Eastern'), id='EODTasks', misfire_grace_time = None)
		self._backgroundScheduler.add_job(self._performEODSettlement, 'cron', hour=16, minute=34, timezone=pytz.timezone('US/Eastern'), id='EODSettlement', misfire_grace_time = None)
		BrokerFactory().orderStatusEvent += self._onOrderStatusChanged
		BrokerFactory().commissionReportEvent += self._onCommissionReportEvent
		BrokerFactory().orderExecutionDetailsEvent += self._onOrderExecutionDetailsEvent
		self._lock = asyncio.Lock()
		self._execution_transaction_map = {} # Maps the Execution ID to the Transaction ID

	def shutdown(self):
		"""
		Shutdown the TradeManager. Background scheduler will be stopped
		"""
		logger.debug('Shutting down TradeManager')
		self._backgroundScheduler.remove_all_jobs()
		self._backgroundScheduler.shutdown()

	async def openTrade(self, entryOrder: Order, template: Template):
		brokerConnector = BrokerFactory().getBrokerConnectorByAccount(template.account)
		if brokerConnector == None:
			logger.error(f'No active broker connection found for account {template.account}. Unable to place entry order.')
			return
		
		if brokerConnector.isConnected() == False:
			logger.error(f'Broker connection for account {template.account} is not connected. Unable to place entry order.')
			return
		
		if template.maxOpenTrades > 0:
			openTrades = 0
			for managedTrade in self._trades:
				if managedTrade.template == template and managedTrade.status == 'OPEN':
					openTrades += 1
			if openTrades >= template.maxOpenTrades:
				logger.warning(f'Maximum number of open trades for template {template.name} reached. Unable to place new trade.')
				return

		if brokerConnector.isTradingEnabled() == False:
			logger.error(f'Trading is disabled for account {template.account}. Unable to place entry order.')
			return
		
		orderPrepared = await brokerConnector.prepareOrder(entryOrder)
		if orderPrepared != True:
			logger.error(f'Failed to prepare entry order for account {template.account}. Unable to place entry order.')
			return
		
		logger.info(f'Opening trade at strikes {self._strikes_from_order(entryOrder)}')

		# Midprice calculation and minimum premium check
		entryOrder.price = self._calculateMidPrice(entryOrder)
		logger.info(f'Calculated midprice for entry order: {entryOrder.price}')
		if template.meetsMinimumPremium(entryOrder.price) == False:
			logger.error(f'Entry order for account {template.account} does not meet minimum premium requirement. Unable to place entry order')
			return

		# Create the Trade in the database
		async with self._lock: # Mit Lock arbeiten, damit die Trade IDs nicht doppelt vergeben werden
			with Session(get_db_engine()) as session:
				newTradeSchema = schemas.TradeCreate(account=template.account, symbol=entryOrder.symbol, strategy=template.strategy)
				newTrade = crud.create_trade(session, newTradeSchema)
			newManagedTrade = ManagedTrade(trade=newTrade, entryOrder=entryOrder, template=template)
			self._trades.append(newManagedTrade)
		entryOrder.orderReference = self._composeOrderReference(newManagedTrade, 'Open')
		entryOrderPlaced = await brokerConnector.placeOrder(entryOrder, template)
		if entryOrderPlaced == True:
			logger.debug(f'Entry order for account placed. Now track its execution')
			entryOrder.status = OrderStatus.OPEN
			self._backgroundScheduler.add_job(self._trackEntryOrder, 'interval', seconds=5, id='TrackEntryOrder' + str(newManagedTrade.trade.id), args=[newManagedTrade], max_instances=100)

	def _onCommissionReportEvent(self, order: Order, execution_id: str, commission: float, fee: float):
		"""
		Handles the commission and fee reporting event from the Broker Connector.
		It adds the commission and fee to the transaction in the database.
		"""
		# Determine the transaction based on the execution ID
		try:
			transaction_id = self._execution_transaction_map.get(execution_id)
		except KeyError:
			logger.error(f'No trade transaction found for fill execution id {execution_id}')
			return
		
		for managed_trade in self._trades:
			if order == managed_trade.entryOrder or order == managed_trade.takeProfitOrder or order == managed_trade.stopLossOrder:
				logger.debug(f'Trade {managed_trade.trade.id}: Commission Report for Order received. Commission: {commission} Fee: {fee}')
				with Session(get_db_engine()) as session:
					db_trade = crud.getTrade(session, managed_trade.trade.id)
					transaction = crud.getTransactionById(session, managed_trade.trade.id, transaction_id)
					if transaction == None:
						logger.error('Transaction with id {} for trade {} not found in database!', transactionId, tradeId)
						return
					transaction.commission += commission
					transaction.fee = +fee
					TradeHelper.updateTrade(db_trade)
					session.commit()
					logger.debug(f'Commissions saved to transaction {transaction.id} for trade {managed_trade.trade.id}')
				break

	def _onOrderExecutionDetailsEvent(self, order: Order, execution: Execution):
		"""
		Handles the order execution details which are sent from the Broker Connector
		when a order has been executed.
		"""
		logger.debug(f'Trade Manager Order Execution Details:')
		for managed_trade in self._trades:
			if order == managed_trade.entryOrder or order == managed_trade.takeProfitOrder or order == managed_trade.stopLossOrder:
				logger.debug(f'Trade {managed_trade.trade.id}: Execution Details for Entry Order received')
				with Session(get_db_engine()) as session:
					max_transaction_id = crud.getMaxTransactionId(session, managed_trade.trade.id)
					db_trade = crud.getTrade(session, managed_trade.trade.id)
					if max_transaction_id == 0:
						# Opening transacrion of the trade
						db_trade.status = 'OPEN'
					max_transaction_id += 1
					new_transaction = schemas.TransactionCreate(tradeid=managed_trade.trade.id, transactionid=max_transaction_id,
																id=max_transaction_id,
																symbol=order.symbol,
																type=execution.action,
																sectype=execution.sec_type,
																contracts=execution.amount,
																price=execution.price, 
																expiration=execution.expiration,
																strike=execution.strike,
																fee=0,
																commission=0,
																notes='',
																timestamp=execution.timestamp)
					self._execution_transaction_map[execution.id] = new_transaction.id # Memorize the the Execution ID for later commission report
					crud.createTransaction(session, new_transaction)

					# Check if trade is closed with all these transactions
					TradeHelper.updateTrade(db_trade)
					session.commit()
					if order == managed_trade.entryOrder:
						self._backgroundScheduler.add_job(self._reportExecutedTrade, id='ReportTrade' + str(managed_trade.trade.id) + '-' + execution.id, args=[managed_trade, execution.amount], misfire_grace_time = None, max_instances=100)

	async def _onOrderStatusChanged(self, order: Order, status: OrderStatus, filledAmount: int = 0):
		"""
		Handles the status change event of an order
		"""
		logger.debug(f'Trade Manager Order status changed: {order.symbol} - {status}')
		for managedTrade in self._trades:
			brokerConnector = BrokerFactory().getBrokerConnectorByAccount(managedTrade.template.account)
			if managedTrade.entryOrder == order:
				if status == OrderStatus.CANCELLED and managedTrade.status != 'OPEN':
					managedTrade.entryOrder.status = OrderStatus.CANCELLED
					logger.debug(f'Entry order for trade {managedTrade.trade.id} was cancelled. Deleting trade from databsase')
					try:
						self._backgroundScheduler.remove_job('TrackEntryOrder' + str(managedTrade.trade.id))
					except Exception as e:
						pass
					with Session(get_db_engine()) as session:
						crud.delete_trade(session, managedTrade.trade)
					self._trades.remove(managedTrade)
				if status == OrderStatus.FILLED:
					managedTrade.entryOrder.status = OrderStatus.FILLED
					logger.info(f'Entry Order of trade {managedTrade.trade.id} has been filled at ${managedTrade.entryOrder.averageFillPrice} (Qty: {filledAmount}) and trade is now running.' )
					managedTrade.status = 'OPEN'
					managedTrade.trade.status = 'OPEN'
					with Session(get_db_engine()) as session:
						crud.update_trade(session, managedTrade.trade)
					
					logger.debug('Create TP SL Order Job')
					self._backgroundScheduler.add_job(self._createTakeProfitAndStop, id='CreateTakeProfitAndStop' + str(managedTrade.trade.id), args=[managedTrade], misfire_grace_time = None)
			elif managedTrade.takeProfitOrder == order:
				if status == OrderStatus.FILLED:
					managedTrade.takeProfitOrder.status = OrderStatus.FILLED
					logger.debug(f'Take Profit order for trade {managedTrade.trade.id} was filled. Closing trade now')
					managedTrade.status = 'CLOSED'
					managedTrade.trade.status = 'CLOSED'
					with Session(get_db_engine()) as session:
						crud.update_trade(session, managedTrade.trade)
					logger.success('Take Profit Order has been filled. Trade with id {} finished', managedTrade.trade.id)
				elif status == OrderStatus.CANCELLED:
					managedTrade.takeProfitOrder.status = OrderStatus.CANCELLED
					logger.debug(f'Take Profit order for trade {managedTrade.trade.id} was cancelled.')
				if status == OrderStatus.FILLED or status == OrderStatus.CANCELLED:
					if not brokerConnector.uses_oco_orders() and managedTrade.stopLossOrder:
						logger.info(f'Trade {managedTrade.trade.id} does not use OCO orders. Cancelling Stop Loss order')
						await brokerConnector.cancel_order(managedTrade.stopLossOrder)

			elif managedTrade.stopLossOrder == order:
				if status == OrderStatus.FILLED:
					managedTrade.stopLossOrder.status = OrderStatus.FILLED
					logger.debug(f'Stop Loss order for trade {managedTrade.trade.id} was filled. Closing trade now')
					managedTrade.status = 'CLOSED'
					managedTrade.trade.status = 'CLOSED'
					with Session(get_db_engine()) as session:
						crud.update_trade(session, managedTrade.trade)
					logger.error('Stop Loss Order has been filled. Trade with id {} finished', managedTrade.trade.id)
				elif status == OrderStatus.CANCELLED:
					managedTrade.stopLossOrder.status = OrderStatus.CANCELLED
					logger.debug(f'Stop Loss order for trade {managedTrade.trade.id} was cancelled')
				if status == OrderStatus.FILLED or status == OrderStatus.CANCELLED:
					if not brokerConnector.uses_oco_orders() and managedTrade.takeProfitOrder:
						logger.info(f'Trade {managedTrade.trade.id} does not use OCO orders. Cancelling Take Profit order')
						await brokerConnector.cancel_order(managedTrade.takeProfitOrder)


	def getManagedTrades(self) -> List[ManagedTrade]:
		"""
		Returns a list of all trades currenty managed by the TradeManager 
		"""
		return self._trades
	
	def _calculateMidPrice(self, order: Order) -> float:
		"""
		Calculates the midprice for the given order
		"""
		midPrice = 0
		for leg in order.legs:
			legMidPrice = (leg.askPrice + leg.bidPrice) / 2
			if leg.action == OrderAction.SELL:
				midPrice -= legMidPrice
			else:
				midPrice += legMidPrice
		roundBase = 5
		if len(order.legs) == 1:
			roundBase = 10
		return OptionHelper.roundToTickSize(midPrice, roundBase)
	
	async def _check_and_adjust_stoploss(self, managedTrade: ManagedTrade):
		"""
		Checks if there are Stop Loss adjusters in the template of the trade and if any adjustment of the stop loss is required.
		If so it performs the adjustment of the stoploss order.
		"""
		stoploss_adjusters = managedTrade.template.get_stoploss_adjusters()
		if len(stoploss_adjusters) > 0:
			for adjuster in stoploss_adjusters:
				# Find first adjuster which has not been triggered yet
				if not adjuster.isTriggered():
					#adjusted_stoploss_price = adjuster.execute(managedTrade.currentPrice)
					break

	def _composeOrderReference(self, managedTrade: ManagedTrade, action: str) -> str:
		"""
		Composes the order reference for the given trade and action
		"""
		orderReference = 'OTB (' + str(managedTrade.trade.id) + '): ' + managedTrade.template.name + ' - ' + action
		return orderReference
	
	async def _performEODTasks(self):
		"""
		Performs the end of day tasks at market close
		- Cancel any open orders
		"""
		logger.info('Performing EOD tasks ...')
		has_active_trades = False
		for managedTrade in self._trades:
			if managedTrade.isActive():
				logger.info(f'Trade {managedTrade.trade.id} is still active.')
				has_active_trades = True
				managedTrade.expired = True
				brokerConnector = BrokerFactory().getBrokerConnectorByAccount(managedTrade.template.account)
				if not brokerConnector:
					continue

				if managedTrade.stopLossOrder:
					if managedTrade.stopLossOrder.status != OrderStatus.FILLED:
						logger.info(f'Cancelling Stop Loss order for trade {managedTrade.trade.id}')
						await brokerConnector.cancel_order(managedTrade.stopLossOrder)
				if managedTrade.takeProfitOrder:
					if managedTrade.stopLossOrder and managedTrade.stopLossOrder.ocaGroup == managedTrade.takeProfitOrder.ocaGroup:
						logger.info(f'Take Profit order is cancelled automatically.')
					else:
						if managedTrade.takeProfitOrder.status != OrderStatus.FILLED:
							logger.info(f'Cancelling Take Profit order for trade {managedTrade.trade.id}')
							await brokerConnector.cancel_order(managedTrade.takeProfitOrder)
		if has_active_trades == False:
			logger.info('no active trades found. Nothing to do')

	async def _performEODSettlement(self):
		"""
		Performs the end of day settlement tasks.
		Open Trades, which are expired get settled and closed.
		"""
		logger.info('Performing EOD Settlement ...')
		for managedTrade in self._trades:
			if managedTrade.expired == True and managedTrade.status == 'OPEN':
				logger.info(f'Settling and closing trade {managedTrade.trade.id}')
				broker_connector = BrokerFactory().getBrokerConnectorByAccount(managedTrade.template.account)
				settlement_price = broker_connector.getLastPrice(managedTrade.entryOrder.symbol)
				logger.debug(f'Last price for symbol {managedTrade.entryOrder.symbol} is {settlement_price}')
				managedTrade.status = 'EXPIRED'
				managedTrade.trade.status = 'EXPIRED'
				with Session(get_db_engine()) as session:
					crud.update_trade(session, managedTrade.trade)
				logger.info(f'Trade {managedTrade.trade.id} has been settled and closed.')

		for value in BrokerFactory().get_broker_connectors().values():
			broker_connector: BrokerConnector = value
			if broker_connector.isConnected() == True:
				await broker_connector.eod_settlement_tasks()

	def _strikes_from_order(self, order: Order) -> str:
		"""
		Returns the strike prices from the legs of the given order
		"""
		strikes = ''
		for leg in order.legs:
			if strikes != '':
				strikes += '/'
			strikes += str(leg.strike)
		return strikes

	async def _trackEntryOrder(self, managedTrade: ManagedTrade):
		"""
		Tracks the execution of the entry order
		"""
		jobId = 'TrackEntryOrder' + str(managedTrade.trade.id)
		logger.debug(f'Tracking entry order for trade {managedTrade.trade.id} on account {managedTrade.template.account}')
		if not managedTrade in self._trades:
			logger.info(f'Entry order for trade {managedTrade.trade.id} has been cancelled.')
			self._backgroundScheduler.remove_job(jobId)
			return
		
		if managedTrade.entryOrder.status == OrderStatus.FILLED:
			logger.debug(f'Entry order for trade {managedTrade.trade.id} is filled already. Stop tracking it')
			self._backgroundScheduler.remove_job('TrackEntryOrder' + str(managedTrade.trade.id))
			return

		brokerConnector = BrokerFactory().getBrokerConnectorByAccount(managedTrade.template.account)
		if brokerConnector == None:
			logger.error(f'No active broker connection found for account {managedTrade.template.account}. Unable to adjust entry order')
			return
		
		if brokerConnector.isConnected() == False:
			logger.error(f'Broker connection for account {managedTrade.template.account} is not connected. Unable to adjust entry order')
			return
		
		if brokerConnector.isTradingEnabled() == False:
			logger.error(f'Trading is disabled for account {managedTrade.template.account}. Unable to adjust entry order')
			return
		
		# Angepassten Preis berechnen und prüfen ob er über dem Minimum liegt
		adjustedPrice = OptionHelper.roundToTickSize(managedTrade.entryOrder.price + managedTrade.template.adjustmentStep)
		logger.info('Adjusting entry order. Current Limit Price: {} Adjusted Limit Price: {}', OptionHelper.roundToTickSize(managedTrade.entryOrder.price), adjustedPrice)

		if not managedTrade.template.meetsMinimumPremium(adjustedPrice):
			logger.info('Adjusted price does not meet minimum premium requirement. Canceling entry order')
			# TODO: Implement cancel order
			raise NotImplementedError

		if await brokerConnector.adjustOrder(managedTrade.entryOrder, adjustedPrice) == True:
			managedTrade.entryOrder.price = adjustedPrice
		# # Check if entry order is filled
		# if await brokerConnector.isOrderFilled(managedTrade.entryOrder) == True:
		# 	logger.debug(f'Entry order for account {managedTrade.template.account} is filled')
		# 	self._backgroundScheduler.remove_job('TrackEntryOrder' + managedTrade.trade.id)
		# 	managedTrade.status = 'ENTRY_FILLED'
		# 	# Create exit order
		# 	exitOrder = managedTrade.template

	async def _createTakeProfitAndStop(self, managedTrade: ManagedTrade):
		"""
		Creates the take profit and stop loss orders for the given trade
		"""
		from optrabot.tradetemplate.processor.templateprocessor import TemplateProcessor
		logger.debug(f'Acquiring Lock for TP SL creation for trade {managedTrade.trade.id}')
		async with self._lock:
			logger.debug(f'Creating take profit and stop loss orders for trade {managedTrade.trade.id}')
			brokerConnector = BrokerFactory().getBrokerConnectorByAccount(managedTrade.template.account)
			if brokerConnector == None:
				logger.error(f'No active broker connection found for account {managedTrade.template.account}. Unable to create take profit and stop loss orders')
				return
			
			fillPrice = brokerConnector.getFillPrice(managedTrade.entryOrder)
			logger.debug(f'Fill price for entry order was {fillPrice}')

			templateProcessor = TemplateProcessor().createTemplateProcessor(managedTrade.template)

			# Create and Prepare the Take Profit Order if a take profit is defined in the template
			if managedTrade.template.hasTakeProfit():
				managedTrade.takeProfitOrder = templateProcessor.composeTakeProfitOrder(managedTrade, fillPrice)
				managedTrade.takeProfitOrder.orderReference = self._composeOrderReference(managedTrade, 'TP')
			
				orderPrepared = await brokerConnector.prepareOrder(managedTrade.takeProfitOrder)
				if orderPrepared != True:
					logger.error(f'Failed to prepare take profit order.')
					return
			else:
				logger.info(f'Template {managedTrade.template.name} does not have a take profit defined. No take profit order will be created.')
			
			# Create and Prepare the Stop Loss Order
			if managedTrade.template.hasStopLoss():
				managedTrade.stopLossOrder = templateProcessor.composeStopLossOrder(managedTrade, fillPrice)
				managedTrade.stopLossOrder.orderReference = self._composeOrderReference(managedTrade, 'SL')
				orderPrepared = await brokerConnector.prepareOrder(managedTrade.stopLossOrder)
				if orderPrepared != True:
					logger.error(f'Failed to prepare stop loss order.')
					return
			else:
				logger.info(f'Template {managedTrade.template.name} does not have a stop loss defined. No stop loss order will be created.')
			
			# Set an OCA Group for the Take Profit and Stop Loss Orders if both are defined
			if managedTrade.takeProfitOrder != None and managedTrade.stopLossOrder != None:
				now = datetime.now()
				ocaGroup = str(managedTrade.trade.id) + '_' + now.strftime('%H%M%S')
				managedTrade.takeProfitOrder.ocaGroup = ocaGroup
				managedTrade.stopLossOrder.ocaGroup = ocaGroup

			if managedTrade.takeProfitOrder != None:
				orderPlaced = await brokerConnector.placeOrder(managedTrade.takeProfitOrder, managedTrade.template)
				if orderPlaced == True:
					logger.debug(f'Take Profit order for account placed.')

			if managedTrade.stopLossOrder != None:
				orderPlaced = await brokerConnector.placeOrder(managedTrade.stopLossOrder, managedTrade.template)
				if orderPlaced == True:
					logger.debug(f'Stop Loss order for account placed.')
		logger.debug(f'Releasing Lock for TP SL creation for trade {managedTrade.trade.id}')

	async def _monitorOpenTrades(self):
		"""
		Monitors the open trades and their orders
		"""
		for managedTrade in self._trades:
			if managedTrade.status != 'OPEN' or managedTrade.expired == True:
				continue

			self._update_current_price(managedTrade)

			# Check if stop loss order is in place
			if managedTrade.stopLossOrder != None:
				if managedTrade.stopLossOrder.status == OrderStatus.CANCELLED:
					logger.warning(f'Stop Loss order for open trade {managedTrade.trade.id} was cancelled. Reestablishing it.')
					await self._reestablishStopLossOrder(managedTrade)
				else:
					# Check if the stop loss order needs to be adjusted
					await self._check_and_adjust_stoploss(managedTrade)

			if managedTrade.takeProfitOrder != None:
				if managedTrade.takeProfitOrder.status == OrderStatus.CANCELLED:
					logger.warning(f'Take Profit order for open trade {managedTrade.trade.id} was cancelled. Restablishing it.')
					await self._reestablishTakeProfitOrder(managedTrade)

	async def _reestablishStopLossOrder(self, managedTrade: ManagedTrade):
		"""
		Reestablishes the stop loss order for the given trade
		"""
		brokerConnector = BrokerFactory().getBrokerConnectorByAccount(managedTrade.template.account)
		if brokerConnector == None:
			logger.error(f'No active broker connection found for account {managedTrade.template.account}. Unable to reestablish stop loss order')
			return
		
		managedTrade.stopLossOrder.status = OrderStatus.OPEN
		orderPrepared = await brokerConnector.prepareOrder(managedTrade.stopLossOrder)
		if orderPrepared != True:
			logger.error(f'Failed to prepare stop loss order.')
			return
		
		orderPlaced = await brokerConnector.placeOrder(managedTrade.stopLossOrder, managedTrade.template)
		if orderPlaced == True:
			logger.info(f'Stop Loss order for trade {managedTrade.trade.id} reestablished successfully.')

	async def _reestablishTakeProfitOrder(self, managedTrade: ManagedTrade):
		"""
		Reestablishes the take profit order for the given trade
		"""
		brokerConnector = BrokerFactory().getBrokerConnectorByAccount(managedTrade.template.account)
		if brokerConnector == None:
			logger.error(f'No active broker connection found for account {managedTrade.template.account}. Unable to reestablish stop loss order')
			return
		
		managedTrade.takeProfitOrder.status = OrderStatus.OPEN
		orderPrepared = await brokerConnector.prepareOrder(managedTrade.takeProfitOrder)
		if orderPrepared != True:
			logger.error(f'Failed to prepare take profit order.')
			return
		
		orderPlaced = await brokerConnector.placeOrder(managedTrade.takeProfitOrder, managedTrade.template)
		if orderPlaced == True:
			logger.info(f'Take Profit order for trade {managedTrade.trade.id} reestablished successfully.')

	async def _reportExecutedTrade(self, managedTrade: ManagedTrade, contracts: int):
		"""
		Reports the filled amount of the executed trade to the OptraBot Hub
		It tries to report the event 3 times before giving up.
		"""
		from optrabot.tradinghubclient import TradinghubClient
		
		#executedContracts = 0
		#for leg in managedTrade.entryOrder.legs:
		#	executedContracts += abs(leg.quantity * filledAmount)

		additional_data = {
			'trade_id': managedTrade.trade.id,
			'account': managedTrade.template.account,
			'contracts': int(contracts)
		}
		reporterror = False
		tryCount = 0
		while tryCount < 3:
			try:
				await TradinghubClient().reportAction('CT', additional_data=json.dumps(additional_data))
				break
			except Exception as excp:
				reporterror = True
				tryCount += 1
		if reporterror == True:
			logger.error('Error reporting position open event to OptraBot Hub within 3 tries.')

	def _update_current_price(self, managedTrade: ManagedTrade):
		"""
		Updates the current price of the managed Trade based on the price data from the broker
		"""
		brokerConnector = BrokerFactory().getBrokerConnectorByAccount(managedTrade.template.account)
		if brokerConnector == None or brokerConnector.isConnected() == False:
			logger.error(f'No active broker connection found for account {managedTrade.template.account}. Unable to update current price')
			return
		
		
		