import numpy

class Strategy:
    def __init__(self, executor, verbose = False):
        self.executor = executor
        self.verbose = verbose

    def logVerbose(self, msg):
        if self.verbose:
            print msg

    def decide(self, price, predict):
            if self.verbose:
                self.logVerbose("Price is: " + str(price) + " and next predict is: " + str(predict))
            if predict > price and self.executor.getAvailableFiat() == 0.0:
                self.logVerbose("Hold, since no fiat")
            if predict > price and self.executor.getAvailableFiat() > 0.0:
                self.logVerbose("Buy")
                self.executor.buy(price)
            elif predict < price and self.executor.getAvailableCrypto() == 0.0:
                self.logVerbose("Hold, since no crypto")
            elif predict < price and self.executor.getAvailableCrypto() > 0.0:
                self.logVerbose("Sell")
                self.executor.sell(price)
            elif predict == price:
                self.logVerbose("Predicion eq current Price")

    def closeFiat(self, price):
        if self.executor.getAvailableFiat() > 0.0:
            self.logVerbose("Buy remaining")
            self.executor.buy(price)

    def closeCrypto(self, price):
        if self.executor.getAvailableCrypto() > 0.0:
            self.logVerbose("Sell remaining")
            self.executor.sell(price)
