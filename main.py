import candle_stream as cs
import executor as ex
import models as m
import reporter as r
import strategy as s
import trader as t

stream = cs.CandleStream(m.GdaxCandle60, limit = 5000, size = 60)
executor = ex.ExecutorMock(crypto=0.0, fiat=1000.0, market="BTC/EUR")
reporter = r.Reporter("trades-60.tsv")
reporter.setup(crypto=0.0, fiat=1000.0)
executor.setReporter(reporter)
strategy = s.Strategy(executor)

trader = t.Trader(stream, executor, strategy)
trader.setup(retrainWait = 10, decisionWait = 30, LB = 100, testSize = 0.1, epochs = 100, batchSize = 200)
#trader.backtest(plot = True)
trader.run()

print reporter.getTrades()
print executor.getAccountBalance()
