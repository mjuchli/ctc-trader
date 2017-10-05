from order_type import OrderType
from position import Position

class PositionManager:

    def __init__(self, reporter = None):
        self.reporter = reporter
        self.positionsLong = []
        self.positionsShort = []

    def setReporter(self, reporter):
        self.reporter = reporter

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
