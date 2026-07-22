import pandas as pd

from app.visualization import (
    plot_strategy_comparison
)


performance = pd.DataFrame({

    "Strategy": [
        "SMA",
        "RSI",
        "Momentum",
        "Equal Weight",
        "Sharpe Weighted"
    ],


    "Return": [

        4.0359,

        0.4708,

        3.8902,

        2.5986,

        2.9347

    ]

})


performance = performance.set_index(
    "Strategy"
)


plot_strategy_comparison(
    performance
)