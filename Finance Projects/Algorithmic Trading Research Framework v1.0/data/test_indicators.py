from app.data_loader import load_market_data
from app.indicators import build_indicators


df = load_market_data(
    "AAPL"
)


df = build_indicators(
    df
)


print(
    df.tail()
)