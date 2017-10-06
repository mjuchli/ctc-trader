from datetime import datetime
from order_type import OrderType
import peewee as pw
from model import MySQLModelTrader

""" A position is a simplified form of a trade, indicating the holding of a resource """
class Position(MySQLModelTrader):
    orderType = pw.CharField(null=True)
    cty = pw.DecimalField(null=True)
    price = pw.DecimalField(null=True)
    timestamp = pw.DateTimeField(null=True)

    def __str__(self):
        return (str(self.timestamp) + ',' +
                str(self.getType()) + ',' +
                str(self.getCty()) + ',' +
                str(self.getPrice()))

    def create(self, orderType, cty, price, timestamp = str(datetime.now()).split('.')[0]):
        self.orderType = orderType
        self.cty = cty
        self.price = price
        self.timestamp = timestamp
        return self

    def getType(self):
        return self.orderType

    def getTypeOpposite(self):
        if self.getType() == OrderType.BUY:
            return OrderType.SELL
        elif self.getType() == OrderType.SELL:
            return OrderType.BUY

    def getCty(self):
        return self.cty

    def getPrice(self):
        return self.price

    def getTimeStamp(self):
        return self.timestamp

    def setType(self, orderType):
        self.orderType = orderType

    def setCty(self, cty):
        self.cty = cty

    def setPrice(self, price):
        self.price = price

    def setTimeStamp(self, timestamp):
        self.timestamp = timestamp
