from app.data_loader import load_market_data
from app.indicators import build_indicators
from app.strategies import sma_crossover_strategy
from app.risk_management import fixed_position_size



df = load_market_data(
    "AAPL"
)


df = build_indicators(
    df
)


signals = sma_crossover_strategy(
    df
)



positions = fixed_position_size(
    signals,
    allocation=0.20
)



print(
    positions.tail()
)