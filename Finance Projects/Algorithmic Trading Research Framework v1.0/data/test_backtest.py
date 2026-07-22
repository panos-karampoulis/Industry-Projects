from app.data_loader import load_market_data
from app.indicators import build_indicators
from app.strategies import sma_crossover_strategy
from app.backtester import run_backtest
from app.risk_management import fixed_position_size
from app.evaluation import generate_performance_report



df = load_market_data(
    "AAPL"
)


df = build_indicators(
    df
)


signals = sma_crossover_strategy(
    df
)


position_size = fixed_position_size(
    signals,
    allocation=0.20
)



portfolio = run_backtest(
    df["Close"],
    signals,
    size=position_size,
    sl_stop=0.10,
    tp_stop=0.20
)



report = generate_performance_report(
    portfolio
)


for key,value in report.items():

    print(
        key,
        ":",
        value
    )