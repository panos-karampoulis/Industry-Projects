from app.data_loader import load_market_data
from app.indicators import build_indicators

from app.strategies import (
    sma_crossover_strategy
)

from app.backtester import run_backtest

from app.visualization import (
    plot_equity_curve,
    plot_drawdown
)



df = load_market_data(
    "AAPL"
)


df = build_indicators(
    df
)



signals = sma_crossover_strategy(
    df
)



portfolio = run_backtest(
    df["Close"],
    signals
)



plot_equity_curve(
    portfolio
)



plot_drawdown(
    portfolio
)