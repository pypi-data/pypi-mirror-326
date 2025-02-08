from datetime import datetime
from loguru import logger
from optrabot.broker.order import Leg, OptionRight, Order, OrderAction, OrderType, PriceEffect
from optrabot.optionhelper import OptionHelper
from optrabot.signaldata import SignalData
from optrabot.tradetemplate.processor.templateprocessorbase import TemplateProcessorBase
from optrabot.tradetemplate.templatefactory import LongCall, Template
from optrabot.trademanager import ManagedTrade
from typing import List

class LongCallProcessor(TemplateProcessorBase):

	def __init__(self, template: Template):
		"""
		Initializes the Long Call processor with the given template
		"""
		super().__init__(template)

	def composeEntryOrder(self, signalData: SignalData = None):
		"""
		Composes the entry order for the Long Call template
		"""
		super().composeEntryOrder(signalData)
		longCallTemplate :LongCall = self._template
		longStrike = None
		# Long Strike Determination
		if signalData and signalData.strike > 0:
			longStrike = signalData.strike
		else:
			longStrikeData = longCallTemplate.getLongStrikeData()
			if not longStrikeData:
				raise ValueError('Configuration for Long Strike is missing in template!')
			if longStrikeData.offset:
				logger.debug(f'Using Long Strike Offset: {longStrikeData.offset}')
				longStrike = OptionHelper.roundToStrikePrice(signalData.close + longStrikeData.offset)
			if longStrikeData.delta:
				logger.debug(f'Using Long Strike Delta: {longStrikeData.delta}')
				try:
					longStrike = self.get_short_strike_from_delta("SPX", OptionRight.CALL, longStrikeData.delta)
				except ValueError as value_error:
					logger.error(f'Error while determining Short Strike by Delta: {value_error}')
					return None

			if longStrike == None:
				raise ValueError('Long Strike could not be determined!')
			
			logger.debug(f'Using Long Strike: {longStrike}')

			# Now create entry order for the long call
			legs: List[Leg] = []
			legs.append(Leg(action=OrderAction.BUY, strike=longStrike, symbol=self._template.symbol, right=OptionRight.CALL, expiration=datetime.today(), quantity=1))
			entryOrder = Order(symbol=self._template.symbol, legs=legs, action=OrderAction.BUY_TO_OPEN, quantity=self._template.amount, type=OrderType.LIMIT, price_effect=PriceEffect.DEBIT)
		return entryOrder
	
	def composeTakeProfitOrder(self, managedTrade: ManagedTrade, fillPrice: float) -> Order:
		"""
		Composes the take profit order based on the template and the given fill price
		"""
		super().composeTakeProfitOrder(managedTrade, fillPrice)
		logger.debug('Creating take profit order for template {}', self._template.name)
		takeProfitPrice = self._template.calculateTakeProfitPrice(fillPrice)
		logger.debug(f'Calculated take profit price: {takeProfitPrice}')
		tp_order_legs = managedTrade.entryOrder.legs
		tp_order_legs[0].action = OrderAction.SELL_TO_CLOSE
		takeProfitOrder = Order(symbol=self._template.symbol, legs=tp_order_legs, action=OrderAction.SELL_TO_CLOSE, quantity=self._template.amount, type=OrderType.LIMIT, price=takeProfitPrice, price_effect=PriceEffect.CREDIT)
		return takeProfitOrder
	
	def composeStopLossOrder(self, managedTrade: ManagedTrade, fillPrice: float) -> Order:
		"""
		Composes the stop loss order based on the template and the given fill price
		"""
		super().composeStopLossOrder(managedTrade, fillPrice)
		logger.debug('Creating stop loss order for template {}', self._template.name)
		stopLossPrice = self._template.calculateStopLossPrice(fillPrice)
		logger.debug(f'Calculated stop loss price: {stopLossPrice}')
		sl_order_legs = managedTrade.entryOrder.legs
		sl_order_legs[0].action = OrderAction.SELL_TO_CLOSE
		stopLossOrder = Order(symbol=self._template.symbol, legs=sl_order_legs, action=OrderAction.SELL_TO_CLOSE, quantity=self._template.amount, type=OrderType.STOP, price=stopLossPrice, price_effect=PriceEffect.CREDIT)
		return stopLossOrder