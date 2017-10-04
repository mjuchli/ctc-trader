import os
from order_type import *

class Reporter:
    def __init__(self, fileNameTrades = "trades.tsv", fileNamePosition = "positions.tsv"):
        self.trades = []
        self.fileNameTrades = fileNameTrades
        self.fileNamePosition = fileNamePosition

    def setup(self, crypto, fiat):
        self.crypto = crypto
        self.fiat = fiat

    def getTrades(self):
        return self.trades

    def reportTrade(self, trade):
        self.writeTrade(trade)
        self.trades.append(trade)

    def writeTrade(self, trade):
        f = open(self.fileNameTrades, "a")
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

    def reportPositionOpen(self, position):
        self.writePosition(position)

    def reportPositionClose(self, position, oppPosition):
        self.writePosition(position, oppPosition)

    def writePosition(self, position, oppPosition = None):
        f = open(self.fileNamePosition, "a")
        f.write(str(position.timestamp) + '\t' +
                str(position.getType()) + '\t' +
                str(position.getCty()) + '\t' +
                str(position.getPrice()) + '\t')
        # P&L
        if oppPosition:
            pc = oppPosition.getPrice() / position.getPrice() - 1
            net = position.getCty() * pc
            f.write(str(pc) + '\t' + str(pc) + '\t')

        f.write('\n')
        f.close()
