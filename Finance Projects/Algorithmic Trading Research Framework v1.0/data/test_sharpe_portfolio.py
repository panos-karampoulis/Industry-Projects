from app.portfolio_optimizer import (
    calculate_sharpe_weights
)



sharpe_values = {


    "SMA":
    0.8578,


    "RSI":
    0.5628,


    "Momentum":
    0.8094

}



weights = calculate_sharpe_weights(
    sharpe_values
)



print(
    "OPTIMIZED WEIGHTS"
)


print(weights)