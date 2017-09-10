import os
from order_type import *

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
