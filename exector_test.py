import unittest
from executor import *
from trade import *
from position import *
from order_type import *
from position_manager import PositionManager

class ExecutorTest(unittest.TestCase):

    def getExecutorMock(self):
        return ExecutorMock(crypto=10.0, fiat=1000.0, market="BTC/EUR", ctySize = 1)

    def getExecutorMockWithPM(self):
        pm = PositionManager()
        e = self.getExecutorMock()
        e.setPositionManager(pm)
        return e, pm

    def test_buy_trade(self):
        e = self.getExecutorMock()
        t = e.buy(1000)
        self.assertEqual(t.getType(), OrderType.BUY)
        self.assertEqual(t.getCty(), 1)
        self.assertEqual(t.getPrice(), 1000)
        self.assertEqual(t.getFee(), e.getFee()*1000)

    def test_sell_trade(self):
        e = self.getExecutorMock()
        t = e.sell(1000)
        self.assertEqual(t.getType(), OrderType.SELL)
        self.assertEqual(t.getCty(), 1)
        self.assertEqual(t.getPrice(), 1000)
        self.assertEqual(t.getFee(), e.getFee()*1000)

    def test_buy(self):
        e = self.getExecutorMock()
        e.buy(1000)
        self.assertEqual(e.getAvailableFiat(), -e.getFee()*1000)
        self.assertEqual(e.getAvailableCrypto(), 11)

    def test_sell(self):
        e = self.getExecutorMock()
        e.sell(1000)
        self.assertEqual(e.getAvailableFiat(), 2000-e.getFee()*1000)
        self.assertEqual(e.getAvailableCrypto(), 9)

    def test_buy_sell(self):
        e = self.getExecutorMock()
        e.buy(1000)
        e.sell(1000)
        e.buy(1000)
        self.assertEqual(e.getAvailableFiat(), -3*e.getFee()*1000)
        self.assertEqual(e.getAvailableCrypto(), 11)

    def test_position_buy(self):
        e, pm = self.getExecutorMockWithPM()
        e.buyCty(1, 1000)
        ps = pm.getPositions(OrderType.BUY)
        self.assertEqual(len(ps), 1)
        p = ps[0]
        self.assertEqual(p.getType(), OrderType.BUY)
        self.assertEqual(p.getCty(), 1)
        self.assertEqual(p.getPrice(), 1000)

    def test_position_sell(self):
        e, pm = self.getExecutorMockWithPM()
        t = e.sellCty(1, 1000)
        ps = pm.getPositions(t.getType())
        self.assertEqual(len(ps), 1)
        p = ps[0]
        self.assertEqual(p.getType(), OrderType.SELL)
        self.assertEqual(p.getCty(), 1)
        self.assertEqual(p.getPrice(), 1000)

    def test_position_buy_sell(self):
        e, pm = self.getExecutorMockWithPM()
        e.buyCty(1, 1000)
        e.sellCty(1, 1000)
        e.sellCty(1, 1000)
        e.buyCty(1, 1000)
        self.assertEqual(len(pm.getPositions(OrderType.BUY)), 0)
        self.assertEqual(len(pm.getPositions(OrderType.SELL)), 0)

    def test_position_buy_partially(self):
        e, pm = self.getExecutorMockWithPM()
        e.sellCty(2, 1000)
        e.buyCty(1, 1000)
        self.assertEqual(len(pm.getPositions(OrderType.SELL)), 1)
        self.assertEqual(len(pm.getPositions(OrderType.BUY)), 0)
        p = pm.getPositions(OrderType.SELL)[0]
        self.assertEqual(p.getType(), OrderType.SELL)
        self.assertEqual(p.getCty(), 1)
        self.assertEqual(p.getPrice(), 1000)

    def test_position_sell_partially(self):
        e, pm = self.getExecutorMockWithPM()
        e.buyCty(2, 1000)
        e.sellCty(1, 1000)
        self.assertEqual(len(pm.getPositions(OrderType.BUY)), 1)
        self.assertEqual(len(pm.getPositions(OrderType.SELL)), 0)
        p = pm.getPositions(OrderType.BUY)[0]
        self.assertEqual(p.getType(), OrderType.BUY)
        self.assertEqual(p.getCty(), 1)
        self.assertEqual(p.getPrice(), 1000)

    def test_position_close_and_buy(self):
        e, pm = self.getExecutorMockWithPM()
        e.sellCty(1, 1000)
        e.buyCty(2, 1000)
        self.assertEqual(len(pm.getPositions(OrderType.SELL)), 0)
        self.assertEqual(len(pm.getPositions(OrderType.BUY)), 1)
        p = pm.getPositions(OrderType.BUY)[0]
        self.assertEqual(p.getType(), OrderType.BUY)
        self.assertEqual(p.getCty(), 1)
        self.assertEqual(p.getPrice(), 1000)

    def test_position_close_and_sell(self):
        e, pm = self.getExecutorMockWithPM()
        e.buyCty(1, 1000)
        e.sellCty(2, 1000)
        self.assertEqual(len(pm.getPositions(OrderType.BUY)), 0)
        self.assertEqual(len(pm.getPositions(OrderType.SELL)), 1)
        p = pm.getPositions(OrderType.SELL)[0]
        self.assertEqual(p.getType(), OrderType.SELL)
        self.assertEqual(p.getCty(), 1)
        self.assertEqual(p.getPrice(), 1000)

if __name__ == '__main__':
    unittest.main()
