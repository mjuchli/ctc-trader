import ccxt
import os
from enum import Enum
from datetime import datetime

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

class OrderType(Enum):
    BUY = 'buy'
    SELL = 'sell'

class Trade:
    def __init__(self, orderType, cty, price, fee):
        self.orderType = orderType
        self.cty = cty
        self.price = price
        self.fee = fee
        self.timestamp = str(datetime.now()).split('.')[0] #datetime.utcnow()

    def __str__(self):
        return str(self.orderType) + ": " + str(self.cty) + " for " + str(self.price)

    def getType(self):
        return self.orderType

    def getCty(self):
        return self.cty

    def getPrice(self):
        return self.price

    def getFee(self):
        return self.fee

class Reporter:
    def __init__(self, fileName):
        self.trades = []
        self.fileName = fileName

    def setup(self, crypto, fiat):
        self.crypto = crypto
        self.fiat = fiat

    def getTrades(self):
        return self.trades

    def reportTrade(self, trade):
        self.write(trade)
        self.trades.append(trade)

    def write(self, trade):
        f = open(self.fileName, "a")
        tradeId = str(len(self.trades) + 1)
        f.write(
                tradeId + '\t' +
                str(trade.timestamp) + '\t' +
                str(trade.getType()) + '\t' +
                str(trade.getCty()) + '\t' +
                str(trade.getPrice()) + '\t' +
                str(trade.getFee()) + '\t'
                )
        if self.trades and trade.getType() == OrderType.SELL:
            lastTrade = self.trades[-1]
            profit = trade.getCty() * trade.getPrice() - lastTrade.getCty() * lastTrade.getPrice()
            profitNet = trade.getCty() * trade.getPrice() - lastTrade.getCty() * lastTrade.getPrice() - lastTrade.getFee() - trade.getFee()
            f.write(str(profit) + '\t' + str(profitNet))

        f.write('\n')
        f.close()

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
        fee = pc * (amount / price) * self.fee
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
