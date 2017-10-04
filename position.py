from datetime import datetime
from order_type import OrderType

""" A position is a simplified form of a trade, indicating the holding of a resource """
class Position:

    def __init__(self, orderType, cty, price, timestamp = str(datetime.now()).split('.')[0]):
        self.orderType = orderType
        self.cty = cty
        self.price = price
        self.timestamp = timestamp

    def __str__(self):
        return (str(self.timestamp) + ',' +
                str(self.getType()) + ',' +
                str(self.getCty()) + ',' +
                str(self.getPrice()))

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
