import numpy

class Strategy:
    def __init__(self, executor, percentInvest = 1.0):
        self.executor = executor
        self.percentInvest = percentInvest

    def decide(self, price, predict, verbose = False):
            if verbose:
                print "---"
                print "Price is: " + str(price) + " and next predict is: " + str(predict)
                if predict > price and self.executor.getAvailableFiat() == 0.0:
                    print "Hold, since no fiat"
            if predict > price and self.executor.getAvailableFiat() > 0.0:
                if verbose:
                    print "Buy"
                if not self.executor.getReporter().getTrades():
                    self.executor.buy(price, self.percentInvest)
                else:
                    self.executor.buy(price)
            elif predict < price and self.executor.getAvailableCrypto() == 0.0:
                if verbose:
                    print "Hold, since no crypto"
            elif predict < price and self.executor.getAvailableCrypto() > 0.0:
                if verbose:
                    print "Sell"
                if not self.executor.getReporter().getTrades():
                    self.executor.sell(price, self.percentInvest)
                else:
                    self.executor.sell(price)

            elif predict == price:
                if verbose:
                    print "Predicion eq current Price"

    def closeFiat(self, price, verbose = False):
        if self.executor.getAvailableFiat() > 0.0:
            if verbose:
                print "Buy remaining"
            self.executor.buy(price)

    def closeCrypto(self, price, verbose = False):
        if self.executor.getAvailableCrypto() > 0.0:
            if verbose:
                print "Sell remaining"
            self.executor.sell(price)
