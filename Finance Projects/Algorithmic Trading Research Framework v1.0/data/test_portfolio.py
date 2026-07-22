from app.data_loader import load_market_data
from app.indicators import build_indicators

from app.strategies import (
    sma_crossover_strategy,
    rsi_mean_reversion,
    momentum_strategy
)



# Load data

df = load_market_data(
    "AAPL"
)



# Add indicators

df = build_indicators(
    df
)



print(df.columns)



# Strategies

sma = sma_crossover_strategy(
    df
)


rsi = rsi_mean_reversion(
    df
)


mom = momentum_strategy(
    df
)



print("\nSMA Signals")
print(
    sma.tail()
)



print("\nRSI Signals")
print(
    rsi.tail()
)



print("\nMomentum Signals")
print(
    mom.tail()
)