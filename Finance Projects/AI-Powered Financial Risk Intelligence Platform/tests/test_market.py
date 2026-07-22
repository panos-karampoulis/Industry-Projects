from app.market import (
    get_price_history,
    calculate_returns,
    calculate_volatility,
    calculate_max_drawdown
)


symbol = "MSFT"


data = get_price_history(symbol)


returns = calculate_returns(data)


vol = calculate_volatility(
    returns
)


dd = calculate_max_drawdown(
    data
)


print(data.tail())


print("\nVolatility:")
print(
    round(vol*100,2),
    "%"
)


print("\nMax Drawdown:")
print(
    round(dd*100,2),
    "%"
)