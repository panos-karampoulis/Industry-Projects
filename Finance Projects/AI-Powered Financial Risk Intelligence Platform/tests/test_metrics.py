from app.market import (
    get_price_history,
    calculate_returns
)

from app.metrics import (
    calculate_return_statistics
)


symbol = "MSFT"


data = get_price_history(symbol)


returns = calculate_returns(
    data
)


stats = calculate_return_statistics(
    returns
)


print(stats)