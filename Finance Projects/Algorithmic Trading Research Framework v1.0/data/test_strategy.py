from app.data_loader import load_market_data
from app.indicators import build_indicators
from app.strategies import sma_crossover_strategy



df = load_market_data(
    "AAPL"
)


df = build_indicators(
    df
)


signals = sma_crossover_strategy(
    df
)


print(
    signals.tail()
)