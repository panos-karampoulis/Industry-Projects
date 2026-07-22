import pandas as pd

from app.visualization import (
    plot_correlation_heatmap
)



returns = pd.DataFrame({

    "SMA": [

        0.01,
        0.02,
        -0.01,
        0.03

    ],


    "RSI": [

        0.00,
        0.01,
        0.02,
        -0.01

    ],


    "Momentum": [

        0.015,
        0.025,
        -0.015,
        0.035

    ]

})


plot_correlation_heatmap(
    returns
)