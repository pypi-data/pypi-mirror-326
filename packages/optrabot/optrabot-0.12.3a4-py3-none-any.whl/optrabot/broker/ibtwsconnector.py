import asyncio
import datetime as dt
import re
from typing import Dict, List
from optrabot.broker.optionpricedata import OptionStrikeData, OptionStrikePriceData
from optrabot.optionhelper import OptionHelper
from optrabot.broker.brokerconnector import BrokerConnector
from loguru import logger
from ib_async import *
import optrabot.config as optrabotcfg
from optrabot.models import Account
from optrabot.broker.order import Leg, OptionRight, Order as GenericOrder, OrderAction, OrderType, OrderStatus as GenericOrderStatus, Execution
from optrabot.tradetemplate.templatefactory import Template
import optrabot.symbolinfo as symbolInfo

class IBSymbolData:
	def __init__(self) -> None:
		self.symbol: str = None
		self.contract: Contract = None
		self.option_trading_class: str = None
		self.ticker: Ticker = None
		self.noPriceDataCount = 0
		self.lastPrice: float = None
		self.optionPriceData: Dict[dt.date, OptionStrikeData] = {}

class ForeignOrder(GenericOrder):
	"""
	Represents an order that has been placed by another user in the TWS.
	It is just used for managing conflicting orders.
	"""
	def __init__(self) -> None:
		super().__init__()

class IBTWSTConnector(BrokerConnector):
	def __init__(self) -> None:
		super().__init__()
		self._host = ''
		self._port = None
		self._clientid = None
		self._initialize()
		self.id = 'IBTWS'
		self.broker = 'IBKR'
		self._lock = asyncio.Lock()
		self._ib = IB()
		self._ib.errorEvent += self.onErrorEvent
		self._ib.disconnectedEvent += self.onDisconnected
		self._ib.execDetailsEvent += self.onExecDetailsEvent
		self._ib.orderStatusEvent += self.onOrderStatusEvent
		self._ib.commissionReportEvent += self.onCommissionReportEvent
		self._ib.pendingTickersEvent += self.onPendingTickers
		self._compiled_option_pattern = re.compile(pattern = r'^(?P<optionsymbol>[A-Z]+)\ +(?P<expiration>[0-9]+)(?P<type>[CP])(?P<strike>[0-9]+)')
		self._symbolData: Dict[str, IBSymbolData] = {}
		self._symbolReverseLookup: Dict[str, str] = {}		# maps IB symbol to generic symbol
		self._orders: List[GenericOrder] = []
		self._duplicate_order_ids: List[int] = []			# Liste mit Order-IDs, die als dopplete Order IDs von TWS gemeldet wurden
		self._conflictingOrderMap: Dict[GenericOrder,GenericOrder] = {}   # Maps the conflicting order to the causing order

	def ___del__(self):
		"""
		Disconnect from TWS when object is deleted
		"""
		if self._ib.isConnected():
			self._ib.disconnect()

		# Unregister event handlers
		self._ib.errorEvent -= self.onErrorEvent
		self._ib.disconnectedEvent -= self.onDisconnected
		self._ib.execDetailsEvent -= self.onExecDetailsEvent
		self._ib.orderStatusEvent -= self.onOrderStatusEvent
		self._ib.commissionReportEvent -= self.onCommissionReportEvent
		self._ib.pendingTickersEvent -= self.onPendingTickers

	def _initialize(self):
		"""
		Initialize the TWS connector from the configuration
		"""
		config :optrabotcfg.Config = optrabotcfg.appConfig
		try:
			config.get('tws')
		except KeyError as keyErr:
			logger.debug('No TWS connection configured')
			return

		self._host = config.get('tws.host')
		if self._host == '':
			self._host = 'localhost'
		
		try:
			self._port = int(config.get('tws.port'))
		except KeyError as keyErr:
			self._port = 7496
		try:
			self._clientid = int(config.get('tws.clientid'))
		except KeyError as keyErr:
			self._clientid = 21
		self._initialized = True

	async def cancel_order(self, order: GenericOrder):
		""" 
		Cancels the given order
		"""
		await super().cancel_order(order)
		ibTrade: Trade = order.brokerSpecific['trade']
		if ibTrade.orderStatus.status != OrderStatus.Cancelled:
			self._ib.cancelOrder(ibTrade.order)

	async def connect(self):
		await super().connect()
		
		asyncio.create_task(self._connect_tws_task())

	async def disconnect(self):
		await super().disconnect()
		try:
			await self.eod_settlement_tasks()
			self._ib.disconnect()
		except Exception as excp:
			pass

	async def eod_settlement_tasks(self):
		"""
		Perform End of Day settlement tasks.
		- Unsubscribe from expired market data
		"""
		for symbolData in self._symbolData.values():
			try:
				today = dt.date.today()
				todays_option_price_data = symbolData.optionPriceData[today]
				for value in todays_option_price_data.strikeData.values():
					option_price_data: OptionStrikePriceData = value
					try:
						call_contract = option_price_data.brokerSpecific['call_contract']
						if call_contract:
							self._ib.cancelMktData(call_contract)
							option_price_data.brokerSpecific['call_contract'] = None
					except KeyError as keyErr:
						pass
					try:
						put_contract = option_price_data.brokerSpecific['put_contract']
						if put_contract:
							self._ib.cancelMktData(put_contract)
							option_price_data.brokerSpecific['put_contract'] = None
					except KeyError as keyErr:
						pass
			except KeyError as keyErr:
				pass

	def getAccounts(self) -> List[Account]:
		"""
		Returns the accounts managed by the TWS connection
		"""
		if len(self._managedAccounts) == 0 and self.isConnected():
			for managedAccount in self._ib.managedAccounts():
				account = Account(id = managedAccount, name = managedAccount, broker = self.broker, pdt = False)
				self._managedAccounts.append(account)
		return self._managedAccounts

	def isConnected(self) -> bool:
		return self._ib.isConnected()
	
	async def prepareOrder(self, order: GenericOrder) -> bool:
		"""
		Prepares the given order for execution.
		- Retrieve current market data for order legs

		It returns True, if the order could be prepared successfully
		"""
		logger.debug("Wait for lock Prepare Order")
		async with self._lock:
			logger.debug("Got Prepare Order lock")
			try:
				symbolInformation = symbolInfo.symbol_infos[order.symbol]
				symbolData = self._symbolData[order.symbol]
				current_date = dt.date.today()
				#expiration = current_date.strftime('%Y%m%d')
				comboLegs: list[ComboLeg] = []
				comboContracts: list[Contract] = []
				option_price_data = symbolData.optionPriceData[current_date]
				for leg in order.legs:
					#legContract = Option(symbolData.contract.symbol, expiration, leg.strike, self._mappedRight(leg.right), symbolInformation.exchange, tradingClass = self._determineTradingClass(symbolData.contract.symbol))
					option_strike_price_data = option_price_data.strikeData[leg.strike]
					leg_contract = option_strike_price_data.brokerSpecific['call_contract'] if leg.right == OptionRight.CALL else option_strike_price_data.brokerSpecific['put_contract']
					#await self._ib.qualifyContractsAsync(legContract)
					if not OptionHelper.checkContractIsQualified(leg_contract):
						logger.error("Contract {} is not qualified!", leg_contract)
						return False
					
					# Preisdaten für das Order Leg übernehmen
					if not option_strike_price_data.is_outdated():
						leg.askPrice = option_strike_price_data.putAsk if leg.right == OptionRight.PUT else option_strike_price_data.callAsk
						leg.bidPrice = option_strike_price_data.putBid if leg.right == OptionRight.PUT else option_strike_price_data.callBid
					else:
						logger.error("Price data for strike {} is outdated!", leg.strike)
						return False

					comboContracts.append(leg_contract)
					leg.brokerSpecific['contract'] = leg_contract
					comboLeg = ComboLeg(conId=leg_contract.conId, ratio=1, action=self._mappedOrderAction(leg.action), exchange=symbolInformation.exchange)
					comboLegs.append(comboLeg)
				order.brokerSpecific['comboLegs'] = comboLegs
			except Exception as excp:
				logger.error("Error preparing order: {}", excp)
				return False
			
			return True

	async def placeOrder(self, order: GenericOrder, template: Template) -> bool:
		""" 
		Places the given order. It returns True if the entry order has been placed.
		"""
		logger.debug('Wait for Place order lock')
		async with self._lock:
			logger.debug('Got Place order lock')
			symbolInformation = symbolInfo.symbol_infos[order.symbol]
			symbolData = self._symbolData[order.symbol]		
	
			comboLegs = order.brokerSpecific['comboLegs']
			if not comboLegs:
				logger.error("Internal Error: Broker specific attribute comboContracts not filled!")
				return
			
			logger.debug('Checking for open Trades if Combo Legs are colliding')
			#contractsWithOpenOrders = await self._getAllOpenOrderContracts(template.account, symbolData.contract.symbol)

			conflictingOrders = await self._findConflictingOrders(order, template.account)
			if len(conflictingOrders) > 0:
				cancelledOCAs = []
				logger.debug(f'Found {len(conflictingOrders)} conflicting orders for symbol {order.symbol}...adding them to the conflicting order map')
				for conflictingIBTrade in conflictingOrders:
					conflictingOrder = self._findOrderByIBTrade(conflictingIBTrade)
					if conflictingOrder == None:
						logger.error(f'There is a foreign order from another user at the strike prices. Unable to handle it. Trade cannot be placed!')
						return

					self._conflictingOrderMap[conflictingOrder] = order # Conflicting Order mit der verursachenden Order verknüpfen und merken
					
					# Cancel the conflicting order
					if conflictingIBTrade.order.ocaGroup and conflictingIBTrade.order.ocaGroup in cancelledOCAs:
						# Order braucht nicht storniert werden, da bereits eine andere aus der gleichen OCA Gruppe storniert wurde
						pass
					else:
						self._ib.cancelOrder(conflictingIBTrade.order)
						if conflictingIBTrade.order.ocaGroup:
							cancelledOCAs.append(conflictingIBTrade.order.ocaGroup)

				# Urspüngliche Broker Order - Broker Specific [trade] ; Aktuelle Broker Order ; [Conflicting Trades]

				# Ich stormiere die Conflicting Trades
				# - Beim OrderStatusEvent darf die Stonierung für diese Orders nicht weitergreicht werden, weil sie in der Conflicting Trade Map
				#   enthalten sind

				# Es wird die aktuelle Order platziert
				# - Beim OrderStatusEvent "Filled" muss zusätzlich geprüft werden ob es in der Conflicting Trade Map einen Eintrag gibt
				#   wenn ja, dann müssen die referenzierten Conflicting Trades wieder in den Markt gelegt werden

			# Die Orders der behindernden Trades müssen hier storniert werden und deren Daten zwischengespeichert werden
			# Auch der Bezug zu dieser Order, denn wenn diese ausgeführt worden ist müssen die stornierten Orders wieder neu in den Markt gelegt werden.
			#for trade in conflictingTrades:
			#	trade.order.transmit = False
			#	trade.orderStatus.status = OrderStatus.Inactive
			#	self._ib.placeOrder(trade.contract, trade.order)

			#if len(conflictingTrades) > 0:
			#	logger.error(f'Order with opposite action already open for contract. Order not placed!')
			#	return False
			comboContract = None
			if len(order.legs) > 1:
				comboContract = Contract(symbol=symbolData.contract.symbol, secType='BAG', exchange=symbolInformation.exchange, currency=symbolData.contract.currency, comboLegs=comboLegs)
			else:
				comboContract = order.legs[0].brokerSpecific['contract']

			if order.type == OrderType.LIMIT:
				#order.price -= 0.50
				ibOrder = LimitOrder(self._mappedOrderAction(order.action), order.quantity, order.price)
				ibOrder.account = template.account
				ibOrder.outsideRth = True
			elif order.type == OrderType.STOP:
				ibOrder = StopOrder(self._mappedOrderAction(order.action), order.quantity, order.price)
				ibOrder.account = template.account
				ibOrder.outsideRth = True
			else:
				logger.error(f'Order type {order.type} currently not supported by IBKR Connector!')

			ibOrder.orderRef = order.orderReference
			if order.ocaGroup:  # https://interactivebrokers.github.io/tws-api/oca.html
				ibOrder.ocaGroup = order.ocaGroup
				ibOrder.ocaType = 1
			trade = self._ib.placeOrder(comboContract, ibOrder)
			order.brokerSpecific['comboContract'] = comboContract
			order.brokerSpecific['order'] = ibOrder
			order.brokerSpecific['trade'] = trade
			self._orders.append(order)
			logger.debug(f'Account: {template.account} Entry Order {ibOrder.orderId} placed for Trade: {trade} Number of contracts: {order.quantity}')
			return True
	
	async def adjustOrder(self, order: GenericOrder, price: float) -> bool:
		""" 
		Adjusts the given order with the given new price
		"""
		if order.status == GenericOrderStatus.FILLED:
			logger.info('Order {} is already filled. Adjustment not required.', order)
			return True
		if order.status == GenericOrderStatus.CANCELLED:
			logger.info('Order {} is already cancelled. Adjustment not possible.', order)
			return True
		
		trade: Trade = order.brokerSpecific['trade']
		try:
			comboContract = order.brokerSpecific['comboContract']
			ibOrder: Order = order.brokerSpecific['order']
			ibOrder.lmtPrice = price
			trade = self._ib.placeOrder(comboContract, ibOrder)
			order.brokerSpecific['trade'] = trade
			return True
		except Exception as excp:
			logger('Exception beim Anpassen der Order')
		return False

	async def requestTickerData(self, symbols: List[str]):
		"""
		Request ticker data for the given symbols and their options
		"""
		contracts = []
		for symbol in symbols:
			requestOptionsData = False
			optiontradingclass = ''
			match symbol:
				case 'SPX':
					symbolData = IBSymbolData()
					symbolData.symbol = symbol
					symbolInformation = symbolInfo.symbol_infos[symbolData.symbol]
					symbolData.contract = Index('SPX', 'CBOE')
					symbolData.option_trading_class = symbolInformation.trading_class
					self._symbolData[symbol] = symbolData
					self._symbolReverseLookup[symbolData.contract.symbol] = symbol
					contracts.append(symbolData.contract)
				case 'VIX':
					symbolData = IBSymbolData()
					symbolData.symbol = symbol
					symbolData.contract = Index('VIX', 'CBOE')
					self._symbolData[symbol] = symbolData
					self._symbolReverseLookup[symbolData.contract.symbol] = symbol
					contracts.append(symbolData.contract)
				case _:
					logger.error(f'Symbol {symbol} currently not supported by IBKR Connector!')
					continue

		try:
			qualifiedContracts = await self._ib.qualifyContractsAsync(*contracts)
			for contract in qualifiedContracts:
				self._ib.reqMktData(contract, '', False, False)
		except Exception as excp:
			logger.error(f'Error qualifying contract {symbolData.contract}: {excp}')
			return
			
			#self._ib.reqMktData(symbolData.contract, '', False, False)

			# if requestOptionsData:
			# 	chains = await self._ib.reqSecDefOptParamsAsync(symbolData.contract.symbol, '', symbolData.contract.secType, symbolData.contract.conId)
			# 	chain = next(c for c in chains if c.tradingClass == optiontradingclass and c.exchange == 'CBOE')
			# 	if chain == None:
			# 		logger.error(f'No Option Chain for trading class {optiontradingclass} found. Unable to request option data')
			# 		return
				
			# 	current_date = dt.date.today()
			# 	expiration = current_date.strftime('%Y%m%d')

			# 	if int(chain.expirations[0]) > int(expiration):
			# 		logger.warning('There are no SPX options expiring today!')
			# 		return

	async def _connect_tws_task(self):
		try:
			await self._ib.connectAsync(self._host, self._port, clientId=self._clientid)
			self._emitConnectedEvent()
			
		except Exception as excp:
			self._emitConnectFailedEvent()
			#logger.error("Error connecting TWS: {}", excp)
			#attempt += 1
			#logger.error('Connect failed. Retrying {}. attempt in {} seconds', attempt, delaySecs)
			#await asyncio.sleep(delaySecs)
			#asyncio.create_task(self._connect_ib_task(attempt, delaySecs))

	async def onDisconnected(self):
		#logger.warning('Disconnected from TWS, attempting to reconnect in 30 seconds ...')
		self._tradingEnabled = False
		#asyncio.create_task(self._reconnect_ib_task())
		self._emitDisconnectedEvent()

	async def onErrorEvent(self, reqId: int, errorCode: int, errorString: str, contract: Contract):
		if errorCode in {104, 201, 202, 399, 2103, 2104, 2105, 2106, 2107, 2108, 2109, 2157, 2158}:
			# 104: Cannot modify a filled order
			# 201: Order abgewiesen - Grund:Order has been cancelled already, too late to replace
			# 202: Order wurde storniert z.B. TP order bei OCO, wenn SL Order ausgeführt wurde
			# 399: Warnung das die Order nur während der regulären Handelszeiten ausgeführt wird
			# 10147: OrderId ... that needs to be cancelled is not found
			# 2103, 2104, 2105, 2106, 2108, 2158: Marktdatenverbindung ignorieren
			# 2107: Die Verbindung zum HMDS-Datenzentrum is inaktv, sollte jedoch auf Anfrage verfügbar seind
			# 2109: Warnhinweis zu einem Orderereignis außerhalb der regulären Handelszeiten
			# 2157: Verbindung zum Sec-def-Datenzentrum unterbrochen
			return
		elif errorCode == 201:
			# 201: Order rejected - reason:Stop price revision is disallowed after order has triggered
			# 201: Order rejected - reason:We are unable to accept your order. Your Available Funds are in sufficient
			if errorString.find('Margin') > -1:
				logger.error('Order rejected: Insufficient margin!')
				return

		elif errorCode == 10147:
			# Die zu stornierende Order wurde nicht gefunden
			if reqId in self._duplicate_order_ids:
				logger.info(f'Order {reqId}' + ' is a duplicate order ID. Ignoring error event.')
				return

		elif errorCode == 10148:
			# Order that should be cancelled cannot be cancelled
			# Passiert beim Cancel einer TP oder SL Order, wenn sie per OCO Group verbunden sind und eine der Orders bereits
			# storniert wurde

			# Prüfen ob die betreffende Order in den conflicting Orders enthalten ist
			for entry in self._conflictingOrderMap.keys():
				order: GenericOrder = entry
				if order.brokerSpecific['trade'].order.orderId == reqId:
					logger.debug(f'Order {reqId} is conflicting with another order. Ignoring error event.')
					return
		
		elif errorCode == 10168:
			# Für die angeforderten Markdaten besteht kein Abonnement
			logger.error(f'No valid market data subscription for symbol {contract.symbol}')
			self._tradingEnabled = False
			return

		elif errorCode == 1100:
			# Connection between TWS and IB lost.
			logger.warning('Connection between TWS and Interactive Brokers lost -> Trading disabled!')
			self._tradingEnabled = False
			return
		elif errorCode == 1102:
			# Connection between TWS and IB restored
			logger.success('Connection between TWS and Interactive Brokers has been reestablished! -> Trading enabled!')
			self._tradingEnabled = True
			return

		errorData = {'action': 'errorEvent','reqId':reqId, 'errorCode':errorCode, 'errorString':errorString, 'contract': contract}
		logger.error('IB raised following error: {}', errorData)
	
	async def onExecDetailsEvent(self, trade: Trade, fill: Fill):
		""" This eventhandler is called on trade execution.
		The event is raised for each single fill of an order leg
		"""
		logger.debug('Exec Detail for trade {}', trade)
		logger.debug('Fill: {}', fill)

		for order in self._orders:
			brokerSpecificTrade: Trade = order.brokerSpecific['trade']
			if brokerSpecificTrade.order.orderId == trade.order.orderId:
				relevantOrder = order
				break
		if relevantOrder == None:
			logger.debug(f'No managed order matched the execution details event')
			return
		if fill.contract.secType == 'BAG':
			# Do not store inform stion on combo executions
			return
		if fill.execution.side == 'BOT':
			action = OrderAction.BUY
		else:
			action = OrderAction.SELL
		expirationDate = dt.datetime.strptime(fill.contract.lastTradeDateOrContractMonth, '%Y%m%d')
		execution = Execution(id=fill.execution.execId, 
							action=action,
							sec_type=fill.contract.right,
							strike=fill.contract.strike,
							amount=fill.execution.shares,
							price=fill.execution.avgPrice,
							expiration=expirationDate,
							timestamp=fill.execution.time)
		self._emitOrderExecutionDetailsEvent(relevantOrder, execution)

	async def onCommissionReportEvent(self, trade: Trade, fill: Fill, report: CommissionReport):
		"""
		Handles the Commission Report Event
		"""
		logger.debug('Commission Report order id {} and fill {}', trade.order.orderId, fill)
		logger.debug('Commission Report: {}', report)
		for order in self._orders:
			brokerSpecificTrade: Trade = order.brokerSpecific['trade']
			if brokerSpecificTrade.order.orderId == trade.order.orderId:
				relevantOrder = order
				break
		if relevantOrder == None:
			logger.debug(f'No managed order matched the commission report event')
			return

		self._emitCommissionReportEvent(relevantOrder, fill.execution.execId, report.commission, 0)

	async def onOrderStatusEvent(self, trade: Trade):
		"""
		Handles the Order Status Event
		"""
		logger.debug(f'onOrderStatusEvent() Status: {trade.orderStatus.status}')
		relevantOrder: GenericOrder = None
		for order in self._orders:
			brokerSpecificTrade: Trade = order.brokerSpecific['trade']
			if brokerSpecificTrade.order.orderId == trade.order.orderId:
				relevantOrder = order
				break
		if relevantOrder == None:
			logger.debug(f'No managed order matched the status event')
			return
		
		# Prüfen ob die order in der Conflicting Order Map enthalten ist
		if relevantOrder in self._conflictingOrderMap.keys():
			causingOrder = self._conflictingOrderMap[relevantOrder]
			causingOrderOrderId = causingOrder.brokerSpecific['trade'].order.orderId
			logger.debug(f'Order {trade.order.orderId} is conflicting with order {causingOrderOrderId}. Ignoring status event.')
			return

		if trade.orderStatus.status == OrderStatus.Cancelled or trade.orderStatus.status == OrderStatus.Inactive:
			logEntry: TradeLogEntry = None
			for logEntry in trade.log:
				if logEntry.status != 'Cancelled':
					continue
				logger.debug(f'Order Log: {logEntry}')
			if logEntry == None:
				logger.error(f'No log entry found for cancelled order!')
			elif logEntry.errorCode == 103:
				# Error 103, reqId 10292: Doppelt vorhandene Order-ID
				logger.warning('Adjustment of entry order has been rejected, because Duplicate Order-ID.')
				self._duplicate_order_ids.append(trade.order.orderId)
				# In diesem Fall muss die Order sicherheitshalber neu platziert werden
				try:
					self._ib.cancelOrder(trade.order)
				except Exception as excp:
					logger.debug(f'Error cancelling order: {excp}')
				trade.order.orderId = self._ib.client.getReqId()
				logger.debug(f'Replacing order with new Order Id {trade.order.orderId}')
				relevantOrder.brokerSpecific['trade'] = self._ib.placeOrder(trade.contract, trade.order)
				logger.info(f'Order {trade.order.orderId} has been replaced with new Order Id {trade.order.orderId}')
				return
			elif logEntry.errorCode == 104:
				# Error 104: Cannot modify a filled order
				logger.warning(f'Order {trade.order.orderId} has been filled already. Ignoring the Cancelled status event.')
				return

			# Wenn die stornierte Order eine verursachende Order für Conflicting Ordrer(s) ist, dann müssen die stornierten Orders wieder in den Markt gelegt werden
			await self._placeConflictingOrdersAgain(relevantOrder)
		
		filledAmount = 0
		if trade.orderStatus.status == OrderStatus.Filled:
			# Wenn die gefüllte Order eine verursachende Order für conflicting Order(s) ist und sie vollständig ausgeüfhrt wurde,
			# dann müssen die stornierten Orders wieder in den Markt gelegt werden
			await self._placeConflictingOrdersAgain(relevantOrder)

			filledAmount = relevantOrder.quantity - trade.remaining()
			relevantOrder.averageFillPrice = trade.orderStatus.avgFillPrice

		self._emitOrderStatusEvent(relevantOrder, self._genericOrderStatus(trade.orderStatus.status), filledAmount)
		
	def getFillPrice(self, order: GenericOrder) -> float:
		""" 
		Returns the fill price of the given order if it is filled
		"""
		trade: Trade = order.brokerSpecific['trade']
		return trade.orderStatus.avgFillPrice
	
	def getLastPrice(self, symbol: str) -> float:
		""" 
		Returns the last price of the given symbol
		"""
		symbolData = self._symbolData[symbol]
		if symbolData.ticker == None:
			return 0
		if symbolData.ticker.last == None:
			return symbolData.ticker.close
		return symbolData.ticker.last

	def get_strike_by_delta(self, symbol: str, right: str, delta: int) -> float:
		""" 
		Returns the strike price based on the given delta based on the buffered option price data
		"""
		symbolData = self._symbolData[symbol]
		current_date = dt.date.today()
		option_price_data: OptionStrikeData= symbolData.optionPriceData[current_date]
		previous_delta = 0
		previous_strike = 0
		reverse = True if right == OptionRight.PUT else False
		sorted_strikes = dict(sorted(option_price_data.strikeData.items(), reverse=reverse))
		for strike, price_data in sorted_strikes.items():
			if right == OptionRight.PUT:
				if price_data.putDelta == None:
					continue
				adjusted_delta = price_data.putDelta * -100
			else:
				if price_data.callDelta == None:
					continue
				adjusted_delta = price_data.callDelta * 100
			if adjusted_delta <= delta:
				if OptionHelper.closest_number(delta, previous_delta, adjusted_delta) == adjusted_delta:
					return strike
				else:
					return previous_strike
			previous_delta = adjusted_delta
			previous_strike = strike

		raise ValueError(f'No strike price found for delta {delta} in symbol {symbol}!')

	async def onPendingTickers(self, tickers: List[Ticker]):
		"""
		Handles the pending tickers event
		"""
		for ticker in tickers:
			if ticker.contract.symbol in self._symbolData.keys():
				logger.trace(f'Ticker for symbol {ticker.contract.symbol} received.')
				self._tradingEnabled = True
				ticker.lastExchange
				logger.trace(f'Ticker Last {ticker.last}: {ticker}')
				symbolData = self._symbolData[ticker.contract.symbol]
				symbolData.ticker = ticker
				if ticker.last:
					symbolData.lastPrice = ticker.last
				else:
					symbolData.lastPrice = ticker.close

				# Prüfen ob Preisdaten vorhanden sind
				lastPrice = symbolData.ticker.last
				if util.isNan(lastPrice):
					lastPrice = symbolData.ticker.close
				if util.isNan(lastPrice) and ticker.contract.secType != 'OPT':
					# Wenn mehrmals keine gültigen Preisdaten empfangen wurden, dann wird der Handel deaktiviert
					symbolData.noPriceDataCount += 1
					if symbolData.noPriceDataCount > 5:
						logger.error(f'Receiving no valid price data for symbol {symbolData.symbol}. Trading disabled!')
						self._tradingEnabled = False
						break
					continue
				else:
					symbolData.noPriceDataCount = 0
					self._tradingEnabled = True

				# Für VIX werden keine weiteren Daten gelesen
				if ticker.contract.symbol == 'VIX':
					break

				if ticker.contract.secType != 'OPT':
					# Keine Optionen -> Fehlende Optionen abfragen

					# Symbol anhand der Contract ID ermitteln
					try:
						genericSymbol = self._symbolReverseLookup[ticker.contract.symbol]
						symbolData: IBSymbolData = self._symbolData[genericSymbol]
						expirationDate = dt.date.today()
						atmStrike = OptionHelper.roundToStrikePrice(lastPrice)
						await self._requestMissingOptionData(symbolData, expirationDate, atmStrike)
					except KeyError as keyErr:
						logger.error(f'No generic symbol found for IB TWS symbol {ticker.contract.symbol}')
				else:
					# Option verarbeiten
					try:
						optionType, expiration, strike = self._getOptionInfos(ticker.contract)
					except Exception as exc:
						logger.error(f'Error getting option infos: {exc}')
					genericSymbol = self._symbolReverseLookup[ticker.contract.symbol]
					symbolData: IBSymbolData = self._symbolData[genericSymbol]
					optionStrikeData = symbolData.optionPriceData[expiration]
					optionStrikePriceData = optionStrikeData.strikeData[strike]
					
					if optionType == OptionRight.CALL:
						optionStrikePriceData.callAsk = ticker.ask
						optionStrikePriceData.callBid = ticker.bid
						if ticker.modelGreeks:
							optionStrikePriceData.callDelta = ticker.modelGreeks.delta
					else:
						optionStrikePriceData.putAsk = ticker.ask
						optionStrikePriceData.putBid = ticker.bid
						if ticker.modelGreeks:
							optionStrikePriceData.putDelta = ticker.modelGreeks.delta
					optionStrikePriceData.lastUpdated = dt.datetime.now()
					
	def uses_oco_orders(self) -> bool:
		""" 
		The TWS Connector uses OCO orders for take profit and stop loss orders
		"""
		return True
	
	def _createReplacementOrder(self, ibOrder: Order) -> Order:
		"""
		Creates a new replacement order for the given order
		"""
		if isinstance(ibOrder, LimitOrder):
			replacementOrder = LimitOrder(ibOrder.action, ibOrder.totalQuantity, ibOrder.lmtPrice)
		elif isinstance(ibOrder, StopOrder):
			replacementOrder = StopOrder(ibOrder.action, ibOrder.totalQuantity, ibOrder.auxPrice)
		else:
			logger.error(f'Order type {type(ibOrder)} currently not supported by IBKR Connector!')
			return None
		replacementOrder.account = ibOrder.account
		replacementOrder.outsideRth = ibOrder.outsideRth
		replacementOrder.orderRef = ibOrder.orderRef
		replacementOrder.ocaGroup = ibOrder.ocaGroup
		replacementOrder.ocaType = ibOrder.ocaType
		replacementOrder.transmit = True
		return replacementOrder

	def _findOrderByIBTrade(self, trade: Trade) -> GenericOrder:
		"""
		Find the generic order that belongs to the given IBKR trade
		"""
		for order in self._orders:
			if order.brokerSpecific['trade'] == trade:
				return order
		return None

	async def _findConflictingOrders(self, order: GenericOrder, account: str) -> List[Trade]:
		"""
		Find all open trades for the given account and symbol that are conflicting with the given order
		"""
		comboLegs = order.brokerSpecific['comboLegs']
		oppositeAction = 'BUY' if self._mappedOrderAction(order.action) == 'SELL' else 'SELL'
		conflictingTrades: List[Trade] = []
		openTrades: List[Trade] = await self._ib.reqAllOpenOrdersAsync()
		for openTrade in openTrades:
			if openTrade.order.transmit == False or openTrade.contract.symbol != order.symbol or openTrade.order.account != account or openTrade.order.action != oppositeAction:
				continue

			# ausgeführte und stonierte Trades/Orders spielen keine Rolle (sollten eigentlich nicht mehr in der Liste sein)
			if openTrade.orderStatus.status == OrderStatus.Cancelled or openTrade.orderStatus.status == OrderStatus.Filled:
				continue

			# Offene Order mit entgegengesetzter Aktion gefunden -> Sind enhalten sie Kontrakte die mit der neuen Order kollidieren
			if openTrade.contract.secType == 'BAG':
				for leg in openTrade.contract.comboLegs:
					for comboLeg in comboLegs:
						if leg.conId == comboLeg.conId:
							if openTrade not in conflictingTrades:
								conflictingTrades.append(openTrade)
			else:
				for comboLeg in comboLegs:
					if openTrade.contract.conId == comboLeg.conId:
						if openTrade not in conflictingTrades:
							conflictingTrades.append(openTrade)
		return conflictingTrades

	def _genericOrderStatus(self, status: OrderStatus) -> GenericOrderStatus:
		"""
		Maps the IBKR specific order status to the general order status
		"""
		match status:
			case OrderStatus.PendingSubmit:
				return GenericOrderStatus.OPEN
			case OrderStatus.PreSubmitted:
				return GenericOrderStatus.OPEN
			case OrderStatus.Submitted:
				return GenericOrderStatus.OPEN
			case OrderStatus.ApiCancelled:
				return GenericOrderStatus.CANCELLED
			case OrderStatus.Cancelled:
				return GenericOrderStatus.CANCELLED
			case OrderStatus.Filled:
				return GenericOrderStatus.FILLED
			case OrderStatus.Inactive:
				return GenericOrderStatus.CANCELLED
			case OrderStatus.PendingCancel:
				return GenericOrderStatus.OPEN
			case OrderStatus.Cancelled:
				return GenericOrderStatus.CANCELLED

	def _getOptionInfos(self, option: Option) -> tuple:
		"""
		Extracts the generic symbol and expiration date, strike price from the IBKR option contract
		"""
		error = False
		match = self._compiled_option_pattern.match(option.localSymbol)
		try:
			if match:
				for symbol, symbol_info in symbolInfo.symbol_infos.items():
					if symbol_info.symbol == option.symbol:
						genericSymbol = symbol_info.symbol
						break
				expiration = dt.datetime.strptime(match.group('expiration'), '%y%m%d').date()
				optionType = OptionRight.CALL if match.group('type') == 'C' else OptionRight.PUT
			else:
				raise IndexError
		except IndexError as indexErr:
			logger.error(f'Invalid option symbol {option.localSymbol}')
			error = True
		except ValueError as valueErr:
			logger.error(f'Invalid option symbol {option.localSymbol}')
			error = True
		if genericSymbol == None or error == True:
			raise ValueError(f'Invalid option symbol {option.localSymbol}')
		return optionType, expiration, option.strike

	def _mappedOrderAction(self, action: OrderAction) -> str:
		"""
		Maps the general order action to the IBKR specific order action
		"""
		match action:
			case OrderAction.BUY:
				return 'BUY'
			case OrderAction.BUY_TO_OPEN:
				return 'BUY'
			case OrderAction.SELL:
				return 'SELL'
			case OrderAction.SELL_TO_CLOSE:
				return 'SELL'
			case _:
				logger.error(f'Order action {action} not supported by IBKR Connector!')
				return None
	
	def _mappedRight(self, right: OptionRight) -> str:
		"""
		Maps the general option right to the IBKR specific option right
		"""
		match right:
			case OptionRight.CALL:
				return 'C'
			case OptionRight.PUT:
				return 'P'
			case _:
				raise ValueError(f'Option right {right} not supported by IBKR Connector!')
				return None
			
	async def _placeConflictingOrdersAgain(self, order: GenericOrder):
		"""
		Relevante temporär stornierte Conflicting Orders wieder in den Markt legen, wenn
		die übergebene Order eine verursachende Order ist
		"""
		resolvedConflictingOrders: List[GenericOrder] = []
		for key, value in self._conflictingOrderMap.items():
			if value == order:
				logger.debug(f'Causing order of a conflicting order has been filled. Re-placing conflicting order again.')
				if type(key) == ForeignOrder:
					logger.debug(f'Conflicting order is a foreign order. Re-placing it.')
				conflictingOrder: GenericOrder = key
				ibOrder:Order = conflictingOrder.brokerSpecific['order']
				replacementOrder = self._createReplacementOrder(ibOrder)
				replacementTrade = self._ib.placeOrder(conflictingOrder.brokerSpecific['comboContract'], replacementOrder)
				logger.debug(f'Conflicting order {ibOrder.orderId} has been re-placed with order id {replacementTrade.order.orderId}')
				conflictingOrder.brokerSpecific['order'] = replacementOrder
				conflictingOrder.brokerSpecific['trade'] = replacementTrade
				resolvedConflictingOrders.append(conflictingOrder)
		
		# Jetzt wiedereingestellte conflicting orders aus der Map entfernen
		for entry in resolvedConflictingOrders:
			self._conflictingOrderMap.pop(entry)

	async def _getAllOpenOrderContracts(self, account, symbol) -> List:
		"""
		Determine the ContractIds of all open Orders for the given account and symbol
		"""
		openTrades: List[Trade] = await self._ib.reqAllOpenOrdersAsync()
		openOrderContracts = list()
		for openTrade in openTrades:
			if openTrade.contract.symbol != symbol or openTrade.order.account != account:
				continue
			if openTrade.contract.secType == 'BAG':
				for leg in openTrade.contract.comboLegs:
					openOrderContracts.append(leg.conId)
			else:
				openOrderContracts.append(openTrade.contract.conId)
		return openOrderContracts
	
	def _calculateMidPrice(self, legs: List[Leg], tickers: List[Ticker], contracts: List[Contract]) -> float:
		"""
		Calculates the mid price for the given tickers
		"""
		midPrice = None
		for leg in legs:
			for ticker in tickers:
				if ticker.contract.strike == leg.strike and ticker.contract.right == self._mappedRight(leg.right):
					leg
					legMidPrice = (ticker.ask + ticker.bid) / 2
					if util.isNan(legMidPrice) or (ticker.ask == -1.00 and ticker.bid == -1.00):
						if leg.action == OrderAction.BUY:
							legMidPrice = 0.05
						else:
							return None
					if leg.action == OrderAction.SELL:
						midPrice = -legMidPrice
					else:
						midPrice += legMidPrice
					break

		return OptionHelper.roundToTickSize(midPrice)
	
	async def _requestMissingOptionData(self, symbolData: IBSymbolData, expirationDate: dt.date, atmStrike: float):
		"""
		Request option data for the given symbol and expiration date
		"""
		# Bestehende gespeicherte Optionen abfragen
		try:
			expiration_date_str = expirationDate.strftime('%Y%m%d')
			optionStrikeData = symbolData.optionPriceData[expirationDate]
		except KeyError as keyErr:
			# Wenn noch keine Optionsdaten für das Verfallsdatum vorhanden sind
			# dann bei der TWS anfragen ob es Optionen gibt
			chains = await self._ib.reqSecDefOptParamsAsync(symbolData.contract.symbol, '', symbolData.contract.secType, symbolData.contract.conId)
			try:
				chain = next(c for c in chains if c.tradingClass == symbolData.option_trading_class and c.exchange == symbolData.contract.exchange)
				if int(chain.expirations[0]) > int(expiration_date_str):
					logger.warning('There are no SPX options expiring today!')
					return
				
				optionStrikeData = OptionStrikeData()
				symbolData.optionPriceData[expirationDate] = optionStrikeData
			
			except Exception as excp:
				logger.error(f'Unexpected error: {excp}')
				return
			pass

		# Die 30 Strikes um den ATM Strike herum abfragen
		symbolInformation = symbolInfo.symbol_infos[symbolData.symbol]
		strikesOfInterest = [atmStrike]
		for count in range(1, 30, 1):
			strikePriceAboveATM = atmStrike + (symbolInformation.strike_interval * count)
			strikePriceBelowATM = atmStrike - (symbolInformation.strike_interval * count)
			strikesOfInterest.append(strikePriceAboveATM)
			strikesOfInterest.append(strikePriceBelowATM)
		
		options_to_be_requested = []
		for strikePrice in strikesOfInterest:
			try:
				optionStrikeData.strikeData[strikePrice]
			except KeyError as keyErr:
				option_strike_price_data = OptionStrikePriceData()
				optionStrikeData.strikeData[strikePrice] = option_strike_price_data
				
				call_option_to_be_requested = Option(symbolData.symbol , expiration_date_str, strikePrice, self._mappedRight(OptionRight.CALL), symbolInformation.exchange , tradingClass=symbolData.option_trading_class)
				option_strike_price_data.brokerSpecific['call_contract'] = call_option_to_be_requested
				options_to_be_requested.append(call_option_to_be_requested)
				put_option_to_be_requested = Option(symbolData.symbol , expiration_date_str, strikePrice, self._mappedRight(OptionRight.PUT), symbolInformation.exchange , tradingClass=symbolData.option_trading_class)
				option_strike_price_data.brokerSpecific['put_contract'] = put_option_to_be_requested
				options_to_be_requested.append(put_option_to_be_requested)
		
		if len(options_to_be_requested) > 0:
			qualifiedContracts = await self._ib.qualifyContractsAsync(*options_to_be_requested)
			for qualified_contract in qualifiedContracts:
				self._ib.reqMktData(qualified_contract, '', False, False)