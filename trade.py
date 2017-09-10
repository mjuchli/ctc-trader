from datetime import datetime

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
