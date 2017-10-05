import ccxt
from order_type import *
from trade import *

class Executor:
    def __init__(self, ctySize = 1):
        self.exchange = ccxt.gdax(self.getConfig())
        self.market = self.exchange.market('BTC/EUR')
        self.account_id = '37a4a4f2-7188-44d5-857e-575ea110f9a5'
        self.reporter = None
        self.positionManager = None
        self.ctySize = ctySize

    def getConfig(self):
        return ({
            'apiKey': os.environ['GDAX_KEY'],
            'secret': os.environ['GDAX_SECRET'],
            'password': os.environ['GDAX_PASSPHRASE']
        })

    def getAccountBalance(self):
        balances = (self.exchange.fetchBalance())['info']
        for x in balances:
            if x['id'] == self.account_id:
                return x
        return None

    def getAvailable(self):
        accBalance = self.getAccountBalance()
        if accBalance:
            return self.exchange.decimal(accBalance['available'])
        return None

    def getBalance(self):
        accBalance = self.getAccountBalance()
        if accBalance:
            return self.exchange.decimal(accBalance['balance'])
        return None

    # ----- generic -----
    def getCtySize(self):
        return self.ctySize

    def getFee(self):
        return self.fee

    def getMarket(self):
        return self.market

    def getExchange(self):
        return self.exchange

    def getReporter(self):
        return self.reporter

    def setReporter(self, reporter):
        self.reporter = reporter

    def getPositionManager(self):
        return self.positionManager

    def setPositionManager(self, positionManager):
        self.positionManager = positionManager

    def fillPosition(self, p):
        if self.positionManager:
            self.positionManager.fill(p)

    def reportTrade(self, trade):
        if self.reporter:
            self.reporter.reportTrade(trade)

    def buy(self):
        #amount = self.getAvailable()
        amount = self.exchange.decimal(0.01)
        return self.exchange.create_market_buy_order(self.getMarket(), amount)

    def sell(self):
        return self.exchange.create_market_sell_order(self.getMarket(), self.getAvailable())


class ExecutorMock(Executor):
    def __init__(self, crypto, fiat, market, ctySize = 1, fee = 0.0025):
        self.balance = {}
        self.balance['balance'] = crypto
        self.balance['available'] = crypto
        self.balance['fiat'] = fiat
        self.market = market
        self.ctySize = ctySize
        self.fee = fee
        self.reporter = None
        self.positionManager = None

    def getAccountBalance(self):
        return self.balance

    def getAvailableFiat(self):
        return (self.getAccountBalance())['fiat']

    def getAvailableCrypto(self):
        return (self.getAccountBalance())['balance']

    def buy(self, price):
        return self.buyCty(self.getCtySize(), price)

    def buyCty(self, cty, price):
        amount = cty * price
        fee = amount * self.fee
        self.balance['fiat'] = self.balance['fiat'] - amount - fee
        self.balance['balance'] = self.balance['balance'] + cty
        self.balance['available'] = self.balance['balance']
        t = Trade(OrderType.BUY, cty, price, fee)
        self.fillPosition(t.toPosition())
        self.reportTrade(t)
        return t

    def sell(self, price):
        return self.sellCty(self.getCtySize(), price)

    def sellCty(self, cty, price):
        amount = cty * price
        fee = cty * price * self.fee
        self.balance['balance'] = self.balance['balance'] - cty
        self.balance['available'] = self.balance['balance']
        self.balance['fiat'] = self.balance['fiat'] + amount - fee
        t = Trade(OrderType.SELL, cty, price, fee)
        self.fillPosition(t.toPosition())
        self.reportTrade(t)
        return t
