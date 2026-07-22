from app.data_loader import load_market_data
from app.indicators import build_indicators

from app.strategies import (
    sma_crossover_strategy,
    rsi_mean_reversion,
    momentum_strategy
)

from app.backtester import run_backtest
from app.evaluation import generate_performance_report


import pandas as pd
import vectorbt as vbt



# ==========================
# Load Data
# ==========================

df = load_market_data(
    "AAPL"
)


df = build_indicators(
    df
)



# ==========================
# Generate Signals
# ==========================

sma_signal = sma_crossover_strategy(
    df
)


rsi_signal = rsi_mean_reversion(
    df
)


momentum_signal = momentum_strategy(
    df
)



# ==========================
# Convert Signals to Returns
# ==========================


strategies = {}



for name, signal in {


    "SMA": sma_signal,

    "RSI": rsi_signal,

    "Momentum": momentum_signal


}.items():


    pf = run_backtest(

        df["Close"],

        signal

    )


    strategies[name] = (
        pf.returns()
    )



strategy_returns = pd.DataFrame(
    strategies
)



print("\nStrategy Returns")

print(
    strategy_returns.tail()
)



# ==========================
# Equal Weight Portfolio
# ==========================


weights = {

    "SMA": 1/3,

    "RSI": 1/3,

    "Momentum": 1/3

}



combined_returns = (

    strategy_returns

    *
    pd.Series(weights)

).sum(axis=1)



# ==========================
# Build Portfolio
# ==========================


combined_price = (
    1 + combined_returns
).cumprod() * 100



combined_portfolio = vbt.Portfolio.from_holding(

    combined_price,

    init_cash=10000,

    freq="1D"

)



print("\nCOMBINED PORTFOLIO RESULTS")


print(

    generate_performance_report(
        combined_portfolio
    )

)