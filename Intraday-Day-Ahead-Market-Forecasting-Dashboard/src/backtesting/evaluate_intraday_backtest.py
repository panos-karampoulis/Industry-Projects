import pandas as pd
import numpy as np
import os


BASE_PATH = r"D:\Portfolio\Intraday Market Forecasting - updated"


FILE = os.path.join(
    BASE_PATH,
    "data",
    "backtesting",
    "intraday_backtest_results.csv"
)


df = pd.read_csv(FILE)


print("\n")
print("="*70)
print("INTRADAY MODEL PERFORMANCE")
print("="*70)



for country in df["country"].unique():

    print("\n")
    print("-"*50)
    print(country.upper())
    print("-"*50)


    temp = df[
        df["country"] == country
    ]


    mae = (
        temp["absolute_error"]
        .mean()
    )


    rmse = np.sqrt(
        (
            temp["error"]**2
        ).mean()
    )


    mape = (
        temp["percentage_error"]
        .replace(
            [np.inf,-np.inf],
            np.nan
        )
        .mean()
    )


    bias = (
        temp["error"]
        .mean()
    )


    print(
        f"MAE: {mae:.2f} €/MWh"
    )


    print(
        f"RMSE: {rmse:.2f} €/MWh"
    )


    print(
        f"MAPE: {mape:.2f}%"
    )


    print(
        f"Forecast Bias: {bias:.2f} €/MWh"
    )