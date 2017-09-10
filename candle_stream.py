class CandleStream:
    def __init__(self, candleClass, limit = 0, size = 15):
        self.candleClass = candleClass
        self.limit = limit
        self.size = size

    def getSize(self):
        return self.size

    def get(self):
        return (self.candleClass.select().order_by(self.candleClass.id.desc()).limit(self.limit))[::-1]
