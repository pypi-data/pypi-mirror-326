import asyncio
from dataclasses import dataclass
import datetime as dt
from decimal import Decimal
from typing import Dict, List
from optrabot.optionhelper import OptionHelper
from optrabot.broker.optionpricedata import OptionStrikeData, OptionStrikePriceData
from optrabot.broker.brokerconnector import BrokerConnector
from pydantic import ValidationError
from loguru import logger
from datetime import date, timedelta
import re
from tastytrade import Account, AlertStreamer, DXLinkStreamer, Session
from optrabot.models import Account as ModelAccount
from tastytrade.instruments import NestedOptionChain, NestedOptionChainExpiration, Strike
from tastytrade.utils import TastytradeError
from tastytrade.dxfeed import Greeks, Quote, Candle
from tastytrade.instruments import Option, OptionType
from tastytrade.order import NewOrder, OrderTimeInForce, OrderType, OrderAction, PlacedOrder, OrderStatus
import optrabot.config as optrabotcfg
from optrabot.broker.order import OptionRight, Order as GenericOrder, OrderAction as GenericOrderAction, Leg as GenericOrderLeg, OrderStatus as GenericOrderStatus, PriceEffect
from optrabot.tradetemplate.templatefactory import Template
import optrabot.symbolinfo as symbolInfo

@dataclass
class TastySymbolData:
	def __init__(self) -> None:
		self.symbol: str = None
		self.tastySymbol: str = None
		self.noPriceDataCount: int = 0
		self.optionPriceData: Dict[dt.date, OptionStrikeData] = {}
		self.chain: NestedOptionChain = None
		self.lastPrice: float = 0

class TastytradeConnector(BrokerConnector):
	def __init__(self) -> None:
		super().__init__()
		self._username = ''
		self._password = ''
		self._sandbox = False
		self._initialize()
		self.id = 'TASTY'
		self.broker = 'TASTY'
		self._orders: List[GenericOrder] = []
		self._replacedOrders: List[PlacedOrder] = []
		self._session = None
		self._streamer: DXLinkStreamer = None
		self._alert_streamer: AlertStreamer = None
		self._symbolData: Dict[str, TastySymbolData] = {}
		self._symbolReverseLookup: Dict[str, str] = {}		# maps tastytrade symbol to generic symbol

	def _initialize(self):
		"""
		Initialize the Tastytrade connector from the configuration
		"""
		config :optrabotcfg.Config = optrabotcfg.appConfig
		try:
			config.get('tastytrade')
		except KeyError as keyErr:
			logger.debug('No Tastytrade connection configured')
			return
		
		try:
			self._username = config.get('tastytrade.username')
		except KeyError as keyErr:
			logger.error('Tastytrade username not configured')
			return
		try:
			self._password = config.get('tastytrade.password')
		except KeyError as keyErr:
			logger.error('Tastytrade password not configured')
			return
		
		try:
			self._sandbox = config.get('tastytrade.sandbox')
		except KeyError as keyErr:
			pass
		self._initialized = True

	async def cancel_order(self, order: GenericOrder):
		""" 
		Cancels the given order
		"""
		await super().cancel_order(order)
		tasty_order: PlacedOrder = order.brokerSpecific['order']
		account: Account = order.brokerSpecific['account']
		logger.debug(f'Cancelling order {tasty_order.id}')
		account.delete_order(self._session, tasty_order.id)

	async def connect(self):
		await super().connect()
		try:
			self._session = Session(self._username, self._password, is_test=self._sandbox)
			self._tradingEnabled = True
			self._emitConnectedEvent()
		except TastytradeError as tastyErr:
			logger.error('Failed to connect to Tastytrade: {}', tastyErr)
			self._emitConnectFailedEvent()

	async def disconnect(self):
		await super().disconnect()
		self._tradingEnabled = False
		if self._session != None:
			if self._streamer != None:
				await self._streamer.close()
			if self._alert_streamer != None:
				await self._alert_streamer.close()
			self._session.destroy()
			self._session = None
			self._emitDisconnectedEvent()

	def getAccounts(self) -> List[ModelAccount]:
		"""
		Returns the Tastytrade accounts
		"""
		if len(self._managedAccounts) == 0 and self.isConnected():
			tasty_accounts = Account.get_accounts(self._session)
			for tastyAccount in tasty_accounts:
				account = ModelAccount(id = tastyAccount.account_number, name = tastyAccount.nickname, broker = self.broker, pdt = not tastyAccount.day_trader_status)
				self._managedAccounts.append(account)

			asyncio.create_task(self._request_account_updates(tasty_accounts))
		return self._managedAccounts
	
	def isConnected(self) -> bool:
		if self._session != None:
			return True
		
	async def prepareOrder(self, order: GenericOrder) -> bool:
		"""
		Prepares the given order for execution

		It returns True, if the order could be prepared successfully
		"""
		symbolData = self._symbolData[order.symbol]
		comboLegs: list[GenericOrderLeg] = []
		for leg in order.legs:
			try:
				optionPriceData = symbolData.optionPriceData[leg.expiration.date()]
			except KeyError as keyErr:
				logger.error(f'No option price data for expiration date {leg.expiration.date()} available!')
				return False

			optionInstrument: Option = None
			try:
				priceData: OptionStrikePriceData = optionPriceData.strikeData[leg.strike]
				if not priceData.is_outdated():
					if leg.right == OptionRight.CALL:
						leg.askPrice = float(priceData.callAsk)
						if leg.askPrice == None:
							leg.askPrice = 0
						leg.bidPrice = float(priceData.callBid)
						if leg.bidPrice == None:
							leg.bidPrice = 0
						optionInstrument = Option.get_option(self._session, priceData.brokerSpecific['call_option'])
					elif leg.right == OptionRight.PUT:
						leg.askPrice = float(priceData.putAsk)
						if leg.askPrice == None:
							leg.askPrice = 0
						leg.bidPrice = float(priceData.putBid)
						if leg.bidPrice == None:
							leg.bidPrice = 0
						optionInstrument = Option.get_option(self._session, priceData.brokerSpecific['put_option'])
				else:
					logger.error("Price data for strike {} is outdated or not available!", leg.strike)
					return False

			except KeyError as keyErr:
				# No data for strike available
				logger.error(f'No option price data for strike {leg.strike} available!')
				return False
			except Exception as excp:
				logger.error(f'Error preparing order: {excp}')
				return False
			
			# Build the leg for the tasty trade order
			comboLeg = optionInstrument.build_leg(quantity=Decimal(leg.quantity), action=self._mappedOrderAction(order.action, leg.action))
			comboLegs.append(comboLeg)

		order.brokerSpecific['comboLegs'] = comboLegs

		return True

	async def placeOrder(self, order: GenericOrder, template: Template) -> bool:
		""" 
		Places the given order
		"""
		account = Account.get_account(self._session, template.account)
		new_order_legs = order.brokerSpecific['comboLegs']
		tasty_price = Decimal(order.price * -1 if order.price_effect == PriceEffect.DEBIT else order.price)

		if order.type == OrderType.LIMIT:
			newOrder = NewOrder(
				time_in_force=OrderTimeInForce.DAY,
				order_type=order.type,	
				legs=new_order_legs,
				price=tasty_price
			)
		elif order.type == OrderType.STOP:
			newOrder = NewOrder(
				time_in_force=OrderTimeInForce.DAY,
				order_type=order.type,	
				legs=new_order_legs,
				stop_trigger=tasty_price
			)
		try:
			response = account.place_order(self._session, newOrder, dry_run=False)
			#placedComplexOrders = account.get_live_complex_orders(session=self._session)
			#placedOrders = account.get_live_orders(session=self._session)
			#for order in placedOrders:
			#	logger.debug(f'Live order: {order.id} underlying: {order.underlying_symbol}')
			#	#account.delete_order(session=self._session, order_id=order.id)
			logger.debug(f'Response of place Order: {response}')
			if response.errors:
				for errorMessage in response.errors:
					logger.error(f'Error placing order: {errorMessage}')
					return False
			if response.warnings:
				for warningMessage in response.warnings:
					logger.warning(f'Warning placing order: {warningMessage}')
			
			order.brokerSpecific['order'] = response.order
			order.brokerSpecific['account'] = account
			self._orders.append(order)
			logger.debug(f'Order {response.order.id} placed successfully')
			return True
		except TastytradeError as tastyErr:
			logger.error(f'Error placing order: {tastyErr}')
			return False
		except ValidationError as valErr:
			logger.error(f'Validation error placing order: {valErr}')
			err = valErr.errors()[0]
			logger.error(err)
			#logger.error(repr(valErr.errors()[0]['type']))
			return False 
		except Exception as exc:
			logger.error(f'Unexpected exception placing order: {exc}')
			
			return False
		
	async def adjustOrder(self, order: GenericOrder, price: float) -> bool:
		""" 
		Adjusts the given order with the given new price
		"""
		if order.status == GenericOrderStatus.FILLED:
			logger.info('Order {} is already filled. Adjustment not required.', order)
			return True
		tasty_order: PlacedOrder = order.brokerSpecific['order']
		account: Account = order.brokerSpecific['account']
		logger.debug(f'Adjusting order {tasty_order.id} to price {price}')

		new_order_legs = order.brokerSpecific['comboLegs']
		tasty_price = Decimal(order.price * -1 if order.price_effect == PriceEffect.DEBIT else order.price)
		replacement_order = NewOrder(
			time_in_force=OrderTimeInForce.DAY,
			order_type=OrderType.LIMIT,	
			legs=new_order_legs,
			price=Decimal(price * -1)
		)

		if order.type == OrderType.LIMIT:
			replacement_order = NewOrder(
				time_in_force=OrderTimeInForce.DAY,
				order_type=order.type,	
				legs=new_order_legs,
				price=tasty_price
			)
		elif order.type == OrderType.STOP:
			replacement_order = NewOrder(
				time_in_force=OrderTimeInForce.DAY,
				order_type=order.type,	
				legs=new_order_legs,
				stop_trigger=tasty_price
			)
		try:
			return True
			self._replacedOrders.append(tasty_order)  # Merken für das Cancel Event dieser Order
			response: PlacedOrder = account.replace_order(self._session, tasty_order.id, replacement_order)
			order.brokerSpecific['order'] = response
			self._replacedOrders.append(response) # Auch die neue Order zu den zu ignorierenden Orders hinzufügen
			logger.debug(f'Replacment order {response.id} submitted successfully')
			return True
		
		except TastytradeError as tastyErr:
			logger.error(f'Error adjusting order: {tastyErr}')
			return False
		except ValidationError as valErr:
			logger.error(f'Validation error adjusting order: {valErr}')
			err = valErr.errors()[0]
			logger.error(err)
			return False 
		
	async def requestTickerData(self, symbols: List[str]):
		"""
		Request ticker data for the given symbols and their options
		"""
		self._streamer = await DXLinkStreamer(self._session)

		quote_symbols = []
		candle_symbols = []

		for symbol in symbols:
			match symbol:
				case 'SPX':
					symbolData = TastySymbolData()
					symbolData.symbol = symbol
					symbolData.tastySymbol = 'SPX'
					quote_symbols.append('SPX')
					self._symbolData[symbol] = symbolData
					self._symbolReverseLookup[symbolData.tastySymbol] = symbol
				case 'VIX':
					symbolData = TastySymbolData()
					symbolData.symbol = symbol
					symbolData.tastySymbol = 'VIX'
					candle_symbols.append('VIX')
					self._symbolData[symbol] = symbolData
					self._symbolReverseLookup[symbolData.tastySymbol] = symbol
				case _:
					logger.error(f'Symbol {symbol} currently not supported by Tastytrade Connector!')
					continue

		# subscribe to quotes and greeks for all options on that date
		await self._streamer.subscribe(Quote, quote_symbols)
		await self._streamer.subscribe(Greeks, symbols)
		#await self._streamer.subscribe(Candle, candle_symbols)
		startTime = dt.datetime.now() - timedelta(days=1)
		await self._streamer.subscribe_candle(candle_symbols, interval='1m', start_time=startTime)

		t_listen_quotes = asyncio.create_task(self._update_quotes())
		t_listen_greeks = asyncio.create_task(self._update_greeks())
		t_listen_candle = asyncio.create_task(self._update_candle())
		self._streamerFuture = asyncio.gather(t_listen_quotes, t_listen_greeks, t_listen_candle )

		try:
			await self._streamerFuture
		except asyncio.CancelledError:
			logger.debug('Cancelled listening to quotes and greeks')
		except Exception as exc:
			logger.debug(f'Error listening to quotes and greeks: {exc}')

		# wait we have quotes and greeks for each option
		#while len(self.greeks) != len(options) or len(self.quotes) != len(options):
		#	await asyncio.sleep(0.1)

		#for symbol in symbols:
		#	chain = get_option_chain(self._session, symbol)
		#	pass
		#live_prices = await TastyLivePrices.create(self._session, 'SPX', date(2024, 11, 15))

		#self._streamer = await DXLinkStreamer.create(self._session)
		#await self._streamer.subscribe(Quote, symbols)
		#while True:
		#	quote = await self._streamer.get_event(Quote)
		#	print(quote)
		#listen_quotes_task = asyncio.create_task(self._update_quotes())
		#asyncio.gather(listen_quotes_task)

	async def _update_quotes(self):
		async for e in self._streamer.listen(Quote):
			logger.trace(f'Received Quote: {e.event_symbol} bid price: {e.bid_price} ask price: {e.ask_price}')
			# Preisdaten speichern
			if not e.event_symbol.startswith('.'):
				# Symbol ist ein Basiswert
				try:
					genericSymbol = self._symbolReverseLookup[e.event_symbol]
					symbolData: TastySymbolData  = self._symbolData[genericSymbol]
					midPrice = (e.bid_price + e.ask_price) / 2
					atmStrike = OptionHelper.roundToStrikePrice(midPrice)
					# Prüfen ob Optionsdaten für 10 Strikes vorhanden sind
					#try:
					expirationDate = dt.date.today()
					#		optionPriceDataToday = symbolData.optionPriceData[expirationDate]
					#
					#except KeyError as keyErr:
					#	# Keine Daten für den heutigen Tag vorhanden
					#	logger.debug(f'No option price data for today found for symbol {e.eventSymbol}')
					asyncio.create_task(self._requestMissingOptionData(symbolData, expirationDate, atmStrike))
				except KeyError as keyErr:
					logger.error(f'No generic symbol found for tastytrade symbol {e.event_symbol}')
			else:
				# Symbol ist eine Option
				try:
					symbol, optionType, expiration, strike = self._getOptionInfos(e.event_symbol)
					symbolData = self._symbolData[genericSymbol]
					optionStrikeData = symbolData.optionPriceData[expiration]
					optionStrikePriceData = optionStrikeData.strikeData[strike]
					if optionType == OptionType.CALL:
						optionStrikePriceData.callBid = e.bid_price
						optionStrikePriceData.callAsk = e.ask_price
					else:
						optionStrikePriceData.putBid = e.bid_price
						optionStrikePriceData.putAsk = e.ask_price
					optionStrikePriceData.lastUpdated = dt.datetime.now()
				except Exception as exc:
					logger.error(f'Error getting option infos: {exc}')
	
	async def _update_greeks(self):
		async for e in self._streamer.listen(Greeks):
			logger.debug(f'Received Greeks: {e.event_symbol} delta: {e.delta}')

	async def _update_candle(self):
		async for e in self._streamer.listen(Candle):
			pass
			#logger.debug(f'Received Candle: {e.eventSymbol} close: {e.close}')

	async def _update_accounts(self):
		async for order in self._alert_streamer.listen(PlacedOrder):
			logger.debug(f'Update on Order: {order}')
			#self._updateAccountsInDatabase([account])

	def get_strike_by_delta(self, symbol: str, right: str, delta: int) -> float:
		"""
		Returns the strike price based on the given delta based on the buffered option price data
		"""
		raise NotImplementedError()

	def getFillPrice(self, order: GenericOrder) -> float:
		""" 
		Returns the fill price of the given order if it is filled
		"""
		try:
			tastyOrder: PlacedOrder = order.brokerSpecific['order']
			if tastyOrder.status == OrderStatus.FILLED:
				return abs(float(tastyOrder.price))
			else:
				return 0
		except KeyError as keyErr:
			logger.error(f'No fill price available for order {order}')
	
	def getLastPrice(self, symbol: str) -> float:
		""" 
		Returns the last price of the given symbol
		"""
		try:
			symbolData = self._symbolData[symbol]
			return symbolData.lastPrice
		except KeyError as keyErr:
			logger.error(f'No last price available for symbol {symbol}')
			return 0
	
	def uses_oco_orders(self) -> bool:
		""" 
		Tasty Trade does not use and support OCO orders especially for spreads
		"""
		return False

	async def _requestMissingOptionData(self, symbolData: TastySymbolData, expirationDate: dt.date, atmStrike: float):
		"""
		Request option data for the given symbol and expiration date
		"""
		chain = None
		symbolInformation = symbolInfo.symbol_infos[symbolData.symbol]
		# Bestehende gespeicherte Optionsdaten holen
		try:
			optionStrikeData = symbolData.optionPriceData[expirationDate]
		except KeyError as keyErr:

			# Wenn noch keine Optionsdaten für das Verfallsdatum vorhanden sind, dann bei Tasty anfragen ob es Optionsdaten gibt
			#chains = await a_get_option_chain(self._session, symbolData.tastySymbol)

			# Prüfen ob die Chain für das Symbol bereits abgerufen wurde
			if self._symbolData[symbolData.symbol].chain == None:
				chains = NestedOptionChain.get_chain(self._session, symbolData.tastySymbol)
				for chain in chains:
					if chain.root_symbol == symbolInformation.trading_class:
						break
				assert chain != None
				self._symbolData[symbolData.symbol].chain = chain
			else:
				chain = self._symbolData[symbolData.symbol].chain

			for chain_at_expiration in chain.expirations:
				if chain_at_expiration.expiration_date == expirationDate:
					break

			if chain_at_expiration == None:
				logger.error(f'No options available for symbol {symbolData.tastySymbol} and expiration date {expirationDate}')
				return

			optionStrikeData = OptionStrikeData()
			symbolData.optionPriceData[expirationDate] = optionStrikeData
		
			# Die 20 Strike um den ATM Strike herum abrufen
			symbolInformation = symbolInfo.symbol_infos[symbolData.symbol]
			strikesOfInterest = [atmStrike]
			for count in range(1, 30, 1):
				strikePriceAboveATM = atmStrike + (symbolInformation.strike_interval * count)
				strikePriceBelowATM = atmStrike - (symbolInformation.strike_interval * count)
				strikesOfInterest.append(strikePriceAboveATM)
				strikesOfInterest.append(strikePriceBelowATM)
		
			strikesToBeRequested = []
			for strikePrice in strikesOfInterest:
				try:
					optionStrikeData.strikeData[strikePrice]
				except KeyError as keyErr:
					option_strike_price_data = OptionStrikePriceData()
					optionStrikeData.strikeData[strikePrice] = option_strike_price_data
					strikesToBeRequested.append(strikePrice)

			if len(strikesToBeRequested) > 0:
				streamer_symbols = []
				for item in chain_at_expiration.strikes:
					strike: Strike = item
					if strike.strike_price in strikesToBeRequested:
						option_strike_data = optionStrikeData.strikeData[strike.strike_price]
						option_strike_data.brokerSpecific['call_option'] = strike.call
						option_strike_data.brokerSpecific['put_option'] =  strike.put
						streamer_symbols.append(strike.call_streamer_symbol)
						streamer_symbols.append(strike.put_streamer_symbol)
				await self._streamer.subscribe(Quote, streamer_symbols)
						#strikePriceData = optionStrikeData.strikeData[strike.strike_price]
						#if strike.option_type == OptionType.CALL:
						#	strikePriceData.OptionCall = strike
						#else:
						#	strikePriceData.OptionPut = strike
				#if chain == None:
				#	chain = get_option_chain(self._session, symbolData.tastySymbol)
				#	optionsAtExpiration = [o for o in chain[expirationDate]]

				# streamer_symbols = []
				# for option in optionsAtExpiration:
				# 	if option.strike_price in strikesToBeRequested:
				# 		strikePriceData = optionStrikeData.strikeData[option.strike_price]
				# 		if option.option_type == OptionType.CALL:
				# 			strikePriceData.OptionCall = option
				# 		else:
				# 			strikePriceData.OptionPut = option
				# 		streamer_symbols.append(option.streamer_symbol)
				# await self._streamer.subscribe(Quote, streamer_symbols)

		
	def _getOptionInfos(self, tastySymbol: str) -> tuple:
		"""
		Extracts the generic symbol and expiration date, strike and option side from the tastytrade option symbol.
		If the option symbol information cannot be parsed as expected, a ValueError exception is raised.
		"""
		error = False
		pattern = r'^.(?P<optionsymbol>[A-Z]+)(?P<expiration>[0-9]+)(?P<type>[CP])(?P<strike>[0-9]+)'
		compiledPattern = re.compile(pattern)
		match = compiledPattern.match(tastySymbol)
		try:
			if match:
				optionSymbol = match.group('optionsymbol')
				for symbol, symbol_info in symbolInfo.symbol_infos.items():
					if symbol_info.symbol + symbol_info.option_symbol_suffix == optionSymbol:
						genericSymbol = symbol_info.symbol
						break
				expirationDate = dt.datetime.strptime(match.group('expiration'), '%y%m%d').date()
				strike = float(match.group('strike'))
				optionType = OptionType.CALL if match.group('type') == 'C' else OptionType.PUT
		except IndexError as indexErr:
			logger.error(f'Invalid option symbol {tastySymbol}')
			error = True
		except ValueError as valueErr:
			logger.error(f'Invalid option symbol {tastySymbol}')
			error = True
		if genericSymbol == None or error == True:
			raise ValueError(f'Invalid option symbol {tastySymbol}')
		return genericSymbol, optionType, expirationDate, strike
	
	def _mappedOrderAction(self, orderAction: GenericOrderAction, legAction: GenericOrderAction) -> OrderAction:
		"""
		Maps the general order action to the Tasty specific order action
		"""
		match orderAction:
			case GenericOrderAction.BUY_TO_OPEN:
				if legAction == GenericOrderAction.BUY:
					return OrderAction.BUY_TO_OPEN
				if legAction == GenericOrderAction.SELL:
					return OrderAction.SELL_TO_OPEN
				else:
					raise ValueError(f'Unknown leg action: {legAction}')
			case GenericOrderAction.SELL_TO_OPEN:
				if legAction == GenericOrderAction.SELL:
					return OrderAction.SELL_TO_OPEN
				elif legAction == GenericOrderAction.BUY:
					return OrderAction.BUY_TO_OPEN
				else:
					raise ValueError(f'Unknown leg action: {legAction}')
			case GenericOrderAction.BUY_TO_CLOSE:
				if legAction == GenericOrderAction.BUY:
					return OrderAction.BUY_TO_CLOSE
				if legAction == GenericOrderAction.SELL:
					return OrderAction.SELL_TO_CLOSE
				else:
					raise ValueError(f'Unknown leg action: {legAction}')
			case GenericOrderAction.SELL_TO_CLOSE:
				if legAction == GenericOrderAction.SELL:
					return OrderAction.SELL_TO_CLOSE
				elif legAction == GenericOrderAction.BUY:
					return OrderAction.BUY_TO_CLOSE
				else:
					raise ValueError(f'Unknown leg action: {legAction}')
			case _:
				raise ValueError(f'Unknown order action: {orderAction}')
			
	async def _request_account_updates(self, accounts: List[Account]):
		"""
		Request Account Updates
		"""
		#self._alert_streamer = AlertStreamer(self._session)
		async with AlertStreamer(self._session) as streamer:
			self._alert_streamer = streamer
			await streamer.subscribe_accounts(accounts)
			
			async for order in streamer.listen(PlacedOrder):

				logger.debug(f'Update on order {order.id} status {order.status}')
				ignore_order_event = False
				# Cancel Events von Preisanpassungen ignorieren, da sie kein echtes Cancel sind
				for replaced_order in self._replacedOrders:
					if replaced_order.id == order.id and order.status == OrderStatus.CANCELLED:
						#self._replacedOrders.remove(replaced_order)
						ignore_order_event = True
						logger.debug('Ignoring cancel event for replaced order')
						continue
					if replaced_order.id == order.id and (order.status == OrderStatus.ROUTED or order.status == OrderStatus.LIVE):
						if order.status == OrderStatus.LIVE:
							self._replacedOrders.remove(replaced_order)
						ignore_order_event = True
						logger.debug('Ignoring placement of new replacement order')
						continue
		
				if ignore_order_event == False:
					relevantOrder: GenericOrder = None
					for managedOrder in self._orders:
						#brokerSpecificTrade: Trade = order.brokerSpecific['trade']
						broker_specific_order: PlacedOrder = managedOrder.brokerSpecific['order']
						if broker_specific_order.id == order.id:
							relevantOrder = managedOrder
							break
				
					if relevantOrder == None:
						logger.debug(f'No managed order matched the status event')
					else:
						relevantOrder.brokerSpecific['order'] = order
						filledAmount = int(order.size)
						relevantOrder.averageFillPrice = abs(float(order.price))
						self._emitOrderStatusEvent(relevantOrder, self._genericOrderStatus(order.status), filledAmount)

	def _genericOrderStatus(self, status: OrderStatus) -> GenericOrderStatus:
		"""
		Maps the Tastytrade order status to the generic order status
		"""
		match status:
			case OrderStatus.RECEIVED:
				return GenericOrderStatus.OPEN
			case OrderStatus.LIVE:
				return GenericOrderStatus.OPEN
			case OrderStatus.CANCELLED:
				return GenericOrderStatus.CANCELLED
			case OrderStatus.FILLED:
				return GenericOrderStatus.FILLED