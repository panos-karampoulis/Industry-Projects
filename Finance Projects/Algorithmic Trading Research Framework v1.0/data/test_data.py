from app.data_loader import load_market_data, validate_data


data = load_market_data(
    "AAPL"
)


print(data.head())


print("\nData validation:")

print(
    validate_data(data)
)


print("\nRows:")

print(
    len(data)
)