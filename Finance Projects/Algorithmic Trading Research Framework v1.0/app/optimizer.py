import pandas as pd

from app.indicators import build_indicators
from app.strategies import sma_crossover_strategy
from app.backtester import run_backtest
from app.evaluation import generate_performance_report



def optimize_sma_strategy(
        df,
        fast_windows,
        slow_windows
):


    results = []


    for fast in fast_windows:


        for slow in slow_windows:


            if fast >= slow:
                continue


            data = df.copy()


            data[f"SMA_FAST"] = (
                data["Close"]
                .rolling(fast)
                .mean()
            )


            data[f"SMA_SLOW"] = (
                data["Close"]
                .rolling(slow)
                .mean()
            )



            signals = pd.DataFrame(
                index=data.index
            )


            signals["position"] = 0


            signals.loc[
                data["SMA_FAST"] >
                data["SMA_SLOW"],
                "position"
            ] = 1



            portfolio = run_backtest(

                data["Close"],

                signals

            )


            report = generate_performance_report(
                portfolio
            )


            results.append(

                {

                "Fast SMA": fast,

                "Slow SMA": slow,

                "Sharpe":
                    report["Sharpe Ratio"],

                "Return":
                    report["Total Return"],

                "Drawdown":
                    report["Maximum Drawdown"]

                }

            )


    return pd.DataFrame(results)