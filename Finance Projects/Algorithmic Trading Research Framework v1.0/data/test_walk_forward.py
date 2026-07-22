from app.data_loader import load_market_data
from app.walk_forward import walk_forward_analysis



df = load_market_data(
    "AAPL"
)



results = walk_forward_analysis(
    df
)



print(results)



print("\nAverage Results")

print(
    results[
        [
            "Return",
            "Sharpe",
            "Drawdown"
        ]
    ]
    .replace(
        [float("inf"), -float("inf")],
        0
    )
    .mean()
)