from app.data_loader import load_market_data
from app.optimizer import optimize_sma_strategy



df = load_market_data(
    "AAPL"
)



results = optimize_sma_strategy(

    df,

    fast_windows=[
        20,
        30,
        50,
        70
    ],

    slow_windows=[
        100,
        150,
        200,
        300
    ]

)



print(
    results
    .sort_values(
        "Sharpe",
        ascending=False
    )
    .head(10)
)