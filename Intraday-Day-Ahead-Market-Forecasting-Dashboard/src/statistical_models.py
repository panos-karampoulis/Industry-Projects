from pathlib import Path
import pandas as pd
import numpy as np

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error
)

from statsmodels.tsa.holtwinters import (
    SimpleExpSmoothing,
    ExponentialSmoothing
)

from statsmodels.tsa.arima.model import ARIMA

from statsmodels.tsa.statespace.sarimax import SARIMAX



# ==========================================================
# PATHS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parents[2]

DATA_FILE = (
    BASE_DIR /
    "data" /
    "features" /
    "germany_features.csv"
)


RESULTS_DIR = (
    BASE_DIR /
    "results"
)

RESULTS_DIR.mkdir(
    exist_ok=True
)



# ==========================================================
# METRICS
# ==========================================================

def evaluate(y_true, y_pred):

    mae = mean_absolute_error(
        y_true,
        y_pred
    )

    rmse = np.sqrt(
        mean_squared_error(
            y_true,
            y_pred
        )
    )

    mape = np.mean(
        np.abs(
            (y_true - y_pred)
            /
            y_true
        )
    ) * 100


    return {
        "MAE": mae,
        "RMSE": rmse,
        "MAPE": mape
    }



# ==========================================================
# LOAD DATA
# ==========================================================

df = pd.read_csv(
    DATA_FILE,
    index_col=0,
    parse_dates=True
)


df = df.sort_index()



target = (
    df["day_ahead_price"]
)



# ==========================================================
# TRAIN TEST SPLIT
# ==========================================================

split = int(
    len(target) * 0.8
)


train = target.iloc[:split]

test = target.iloc[split:]



print(
    "Train:",
    train.shape
)

print(
    "Test:",
    test.shape
)



results = []



# ==========================================================
# 1. NAIVE FORECAST
# ==========================================================

naive_pred = pd.Series(
    train.iloc[-1],
    index=test.index
)


metrics = evaluate(
    test,
    naive_pred
)


metrics["Model"] = "Naive"

results.append(metrics)



# ==========================================================
# 2. MOVING AVERAGE
# ==========================================================

window = 24


ma_prediction = pd.Series(
    train
    .rolling(window)
    .mean()
    .iloc[-1],
    index=test.index
)


metrics = evaluate(
    test,
    ma_prediction
)


metrics["Model"] = "Moving Average"

results.append(metrics)



# ==========================================================
# 3. SIMPLE EXPONENTIAL SMOOTHING
# ==========================================================

ses = SimpleExpSmoothing(
    train
)


ses_fit = ses.fit(
    optimized=True
)


ses_forecast = ses_fit.forecast(
    len(test)
)



metrics = evaluate(
    test,
    ses_forecast
)


metrics["Model"] = "Exponential Smoothing"

results.append(metrics)



# ==========================================================
# 4. HOLT-WINTERS
# ==========================================================

hw = ExponentialSmoothing(
    train,
    trend="add",
    seasonal="add",
    seasonal_periods=24
)


hw_fit = hw.fit(
    optimized=True
)


hw_forecast = hw_fit.forecast(
    len(test)
)



metrics = evaluate(
    test,
    hw_forecast
)


metrics["Model"] = "Holt-Winters"

results.append(metrics)



# ==========================================================
# 5. ARIMA
# ==========================================================

print("Running ARIMA...")


arima = ARIMA(
    train,
    order=(2,1,2)
)


arima_fit = arima.fit()


arima_forecast = (
    arima_fit
    .forecast(
        len(test)
    )
)



metrics = evaluate(
    test,
    arima_forecast
)


metrics["Model"] = "ARIMA(2,1,2)"

results.append(metrics)



# ==========================================================
# 6. SARIMA
# ==========================================================

print("Running SARIMA...")


sarima = SARIMAX(
    train,
    order=(1,1,1),
    seasonal_order=(1,1,1,24)
)


sarima_fit = sarima.fit(
    disp=False
)


sarima_forecast = (
    sarima_fit
    .forecast(
        len(test)
    )
)



metrics = evaluate(
    test,
    sarima_forecast
)


metrics["Model"] = "SARIMA"



results.append(metrics)



# ==========================================================
# RESULTS
# ==========================================================

results_df = pd.DataFrame(
    results
)


results_df = results_df[
    [
        "Model",
        "MAE",
        "RMSE",
        "MAPE"
    ]
]


results_df = results_df.sort_values(
    "RMSE"
)



print(
    "\nRESULTS"
)

print(
    results_df
)



results_df.to_csv(
    RESULTS_DIR /
    "statistical_models_results.csv",
    index=False
)


print(
    "\nSaved results."
)