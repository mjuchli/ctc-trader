import candle_stream as cs
import executor as ex
import models as m
import reporter as r
import strategy as s
import trader as t
import label_type as lt

stream = cs.CandleStream(m.GdaxCandle15, size = 1, limit = 1000)
executor = ex.ExecutorMock(crypto=0.0, fiat=1000.0, market="BTC/EUR")
reporter = r.Reporter("trades-15.tsv")
reporter.setup(crypto=0.0, fiat=1000.0)
executor.setReporter(reporter)
strategy = s.Strategy(executor)

trader = t.Trader(stream, executor, strategy)
trader.setup(retrainWait = 5,
             decisionWait = 5,
             LB = 20,
             testSize = 0.1,
             epochs = 1,
             batchSize = 500,
             labelType = lt.LabelType.ClosingPrice)

trader.backtest(plot = True, scaled = True)
#trader.run(plot = False)


#print reporter.getTrades()
#print executor.getAccountBalance()
