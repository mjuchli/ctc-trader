import ccxt
from order_type import *
from trade import *

class Executor:
    def __init__(self):
        self.exchange = ccxt.gdax(self.getConfig())
        self.market = self.exchange.market('BTC/EUR')
        self.account_id = '37a4a4f2-7188-44d5-857e-575ea110f9a5'
        self.reporter = None

    def setReporter(self, reporter):
        self.reporter = reporter

    def getReporter(self):
        return self.reporter

    def report(self, trade):
        if self.reporter:
            self.reporter.reportTrade(trade)

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

    def getMarket(self):
        return self.market

    def getExchange(self):
        return self.exchange

    def buy(self):
        #amount = self.getAvailable()
        amount = self.exchange.decimal(0.01)
        print amount
        return self.exchange.create_market_buy_order(self.getMarket(), amount)

    def sell(self):
        return self.exchange.create_market_sell_order(self.getMarket(), self.getAvailable())

# e = Executor()
# m = e.getExchange()
#
# print e.getAvailable()
# print e.getBalance()
# print e.buy()
# print e.getAccountBalance()


class ExecutorMock(Executor):
    def __init__(self, crypto, fiat, market, fee = 0.0025):
        self.balance = {}
        self.balance['balance'] = crypto
        self.balance['available'] = crypto
        self.balance['fiat'] = fiat
        self.market = market
        self.fee = fee
        self.reporter = None

    def getAccountBalance(self):
        return self.balance

    def getAvailableFiat(self):
        return (self.getAccountBalance())['fiat']

    def getAvailableCrypto(self):
        return (self.getAccountBalance())['balance']

    def buy(self, price, pc = 1.0):
        amount = self.getAvailableFiat()
        cty = pc * (amount / price) * (1-self.fee)
        fee = pc * amount * self.fee
        self.balance['fiat'] = amount - pc * amount
        self.balance['balance'] = self.balance['balance'] + cty
        self.balance['available'] = self.balance['balance']
        t = Trade(OrderType.BUY, cty, price, fee)
        self.report(t)
        return t

    def sell(self, price, pc = 1.0):
        balance = self.getAvailableCrypto()
        cty = pc * balance
        fee = cty * price * self.fee
        self.balance['balance'] = balance - cty
        self.balance['available'] = self.balance['balance']
        self.balance['fiat'] = self.balance['fiat'] + cty * price - fee
        t = Trade(OrderType.SELL, cty, price, fee)
        self.report(t)
        return t

# e = ExecutorMock(crypto=1.0, fiat=0.0, market="BTC/EUR")
# r = Reporter()
# r.setup(crypto=1.0, fiat=0.0)
# e.setReporter(r)
# print e.sell(1000)
# print e.getAvailableFiat()
# print e.getAvailableCrypto()
# print e.buy(1000)
# print e.getAvailableFiat()
# print e.getAvailableCrypto()
#
# print r.getTrades()
