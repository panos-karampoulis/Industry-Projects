from app.data_loader import load_market_data
from app.indicators import build_indicators

from app.strategies import (
    sma_crossover_strategy,
    rsi_mean_reversion,
    momentum_strategy
)

from app.backtester import run_backtest

from app.evaluation import generate_performance_report

from app.portfolio_optimizer import (
    calculate_sharpe_weights
)

import pandas as pd
import vectorbt as vbt



df = load_market_data(
    "AAPL"
)


df = build_indicators(
    df
)



signals = {


"SMA":
sma_crossover_strategy(df),


"RSI":
rsi_mean_reversion(df),


"Momentum":
momentum_strategy(df)

}



returns = {}



for name, signal in signals.items():

    pf = run_backtest(
        df["Close"],
        signal
    )


    returns[name] = pf.returns()



strategy_returns = pd.DataFrame(
    returns
)



weights = calculate_sharpe_weights({

    "SMA":0.8578,

    "RSI":0.5628,

    "Momentum":0.8094

})



print("\nWeights")

print(weights)



portfolio_returns = (

    strategy_returns

    *
    weights

).sum(axis=1)



portfolio_price = (

    1 + portfolio_returns

).cumprod()



optimized_pf = vbt.Portfolio.from_holding(

    portfolio_price,

    init_cash=10000,

    freq="1D"

)



print("\nOPTIMIZED PORTFOLIO")


print(

generate_performance_report(
    optimized_pf
)

)