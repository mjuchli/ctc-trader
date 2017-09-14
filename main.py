import candle_stream as cs
import executor as ex
import models as m
import reporter as r
import strategy as s
import trader as t

stream = cs.CandleStream(m.GdaxCandle15, size = 15, limit = 2000)
executor = ex.ExecutorMock(crypto=0.0, fiat=1000.0, market="BTC/EUR")
reporter = r.Reporter("trades-15.tsv")
reporter.setup(crypto=0.0, fiat=1000.0)
executor.setReporter(reporter)
strategy = s.Strategy(executor)

trader = t.Trader(stream, executor, strategy)
trader.setup(retrainWait = 7,
             decisionWait = 15,
             LB = 15,
             testSize = 0.1,
             epochs = 100,
             batchSize = 500)

trader.backtest(plot = True, scaled = True)
#trader.run()


#print reporter.getTrades()
#print executor.getAccountBalance()
