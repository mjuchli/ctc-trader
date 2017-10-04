import ccxt
from order_type import *
from trade import *
from position import *
class Executor:
    def __init__(self, ctySize = 1):
        self.exchange = ccxt.gdax(self.getConfig())
        self.market = self.exchange.market('BTC/EUR')
        self.account_id = '37a4a4f2-7188-44d5-857e-575ea110f9a5'
        self.reporter = None
        self.positionsLong = []
        self.positionsShort = []
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

    def setReporter(self, reporter):
        self.reporter = reporter

    def getReporter(self):
        return self.reporter

    def reportTrade(self, trade):
        if self.reporter:
            self.reporter.reportTrade(trade)

    def reportPositionOpen(self, position):
        if self.reporter:
            self.reporter.reportPositionOpen(position)

    def reportPositionClose(self, position, oppPosition):
        if self.reporter:
            self.reporter.reportPositionClose(position, oppPosition)

    def getPositions(self, t):
        if t == OrderType.BUY:
            return self.positionsLong
        elif t == OrderType.SELL:
            return self.positionsShort

    def peekPosition(self, t):
        if t == OrderType.BUY:
            return self.positionsLong[0]
        elif t == OrderType.SELL:
            return self.positionsShort[0]

    def addPosition(self, pos):
        if pos.getType() == OrderType.BUY:
            self.positionsLong.append(pos)
        elif pos.getType() == OrderType.SELL:
            self.positionsShort.append(pos)

    def insertPosition(self, pos):
        if pos.getType() == OrderType.BUY:
            self.positionsLong.insert(0, pos)
        elif pos.getType() == OrderType.SELL:
            self.positionsShort.insert(0, pos)

    def popPosition(self, t):
        if t == OrderType.BUY:
            return self.positionsLong.pop(0)
        elif t == OrderType.SELL:
            return self.positionsShort.pop(0)

    def buy(self):
        #amount = self.getAvailable()
        amount = self.exchange.decimal(0.01)
        return self.exchange.create_market_buy_order(self.getMarket(), amount)

    def sell(self):
        return self.exchange.create_market_sell_order(self.getMarket(), self.getAvailable())

    def fill(self, pos):
        """ Upon creation of a trade, this internal operation will try to
            match open position of the opposed side. If an open position of
            the opposed side exists, the aim is to (partially) fill this
            position with the new incoming trade.
        """
        if not self.getPositions(pos.getTypeOpposite()):
            self.addPosition(pos)
            self.reportPositionOpen(pos)
            return [pos]

        lastPosition = self.peekPosition(pos.getTypeOpposite())
        if lastPosition.getCty() == pos.getCty():
            p = self.popPosition(pos.getTypeOpposite())
            self.reportPositionClose(p, pos)
            return [p, pos]
        elif lastPosition.getCty() > pos.getCty():
            remainingCty = lastPosition.getCty() - pos.getCty()
            remainingPosition = Position(lastPosition.orderType, remainingCty, lastPosition.getPrice(), lastPosition.getTimeStamp())
            p = self.popPosition(pos.getTypeOpposite())
            self.reportPositionClose(p, pos)
            self.insertPosition(remainingPosition)
            self.reportPositionOpen(remainingPosition)
            return [p, pos, remainingPosition]
        elif lastPosition.getCty() < pos.getCty():
            remainingCty = pos.getCty() - lastPosition.getCty()
            newPosition = Position(pos.orderType, remainingCty, pos.getPrice())
            p = self.popPosition(pos.getTypeOpposite())
            self.reportPositionClose(p, pos)
            return [p, pos] + self.fill(newPosition)

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
        self.positionsLong = []
        self.positionsShort = []

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
        self.fill(t.toPosition())
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
        self.fill(t.toPosition())
        self.reportTrade(t)
        return t
