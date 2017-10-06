from order_type import OrderType
from position import Position

class PositionManager(object):

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

    def popPosition(self, t):
        if t == OrderType.BUY:
            return self.positionsLong.pop(0)
        elif t == OrderType.SELL:
            return self.positionsShort.pop(0)

    def insertPosition(self, pos):
        """ A local helper function for `updateHead` as lists is being used """
        if pos.getType() == OrderType.BUY:
            self.positionsLong.insert(0, pos)
        elif pos.getType() == OrderType.SELL:
            self.positionsShort.insert(0, pos)

    def updateHeadPosition(self, pos):
        p = self.popPosition(pos.getType())
        self.insertPosition(pos)
        return p

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
            remainingPosition = Position().create(lastPosition.orderType, remainingCty, lastPosition.getPrice(), lastPosition.getTimeStamp())
            p = self.updateHeadPosition(remainingPosition)
            # TODO: self.reportPositionUpdate(p, remainingPosition)
            return [p, remainingPosition]
        elif lastPosition.getCty() < pos.getCty():
            remainingCty = pos.getCty() - lastPosition.getCty()
            newPosition = Position().create(pos.orderType, remainingCty, pos.getPrice())
            p = self.popPosition(pos.getTypeOpposite())
            self.reportPositionClose(p, pos)
            return [p, pos] + self.fill(newPosition)

class PositionDBManager(PositionManager):

    def __init__(self, db, reporter = None):
        super(PositionDBManager, self).__init__(reporter)
        db.get_conn()
        db.create_table(Position, safe=True)

    def getPositions(self, t):
        try:
            query = Position.select().where(Position.orderType == t)#.execute()
            result = list(query)
            return result
        except Position.DoesNotExist:
            return []

    def peekPosition(self, t):
        try:
            return Position.get(Position.orderType == t)
        except Position.DoesNotExist:
            return None

    def addPosition(self, pos):
        pos.save()

    def popPosition(self, t):
        p = self.peekPosition(t)
        if not p:
            return 0
        return p.delete_instance()

    def updateHeadPosition(self, pos):
        return None
