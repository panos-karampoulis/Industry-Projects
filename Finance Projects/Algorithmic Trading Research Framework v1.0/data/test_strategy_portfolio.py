from app.data_loader import load_market_data
from app.indicators import build_indicators

from app.strategies import (
    sma_crossover_strategy,
    rsi_mean_reversion,
    momentum_strategy
)

from app.backtester import run_backtest
from app.evaluation import generate_performance_report



df = load_market_data(
    "AAPL"
)


df = build_indicators(
    df
)



# Strategies

sma_signal = sma_crossover_strategy(df)

rsi_signal = rsi_mean_reversion(df)

momentum_signal = momentum_strategy(df)



# Backtests


sma_portfolio = run_backtest(

    df["Close"],

    sma_signal

)


rsi_portfolio = run_backtest(

    df["Close"],

    rsi_signal

)


momentum_portfolio = run_backtest(

    df["Close"],

    momentum_signal

)



print("\nSMA RESULTS")

print(
    generate_performance_report(
        sma_portfolio
    )
)



print("\nRSI RESULTS")

print(
    generate_performance_report(
        rsi_portfolio
    )
)



print("\nMOMENTUM RESULTS")

print(
    generate_performance_report(
        momentum_portfolio
    )
)