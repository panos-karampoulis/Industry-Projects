import pandas as pd

from app.visualization import (
    plot_contribution
)



contribution = pd.Series({

    "SMA":
    0.000223,


    "RSI":
    0.000048,


    "Momentum":
    0.000224

})


plot_contribution(
    contribution
)