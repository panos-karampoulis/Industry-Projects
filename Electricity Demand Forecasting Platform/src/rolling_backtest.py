import pandas as pd
import joblib

from pathlib import Path

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)


# =======================================
# Paths
# =======================================

BASE_DIR = Path(__file__).resolve().parent.parent

country = "germany"


# =======================================
# Backtest period
# =======================================

end_date = pd.to_datetime(
    "2025-12-31"
)

start_date = end_date - pd.Timedelta(
    days=90
)


# =======================================
# Load dataset
# =======================================

data_file = (
    BASE_DIR
    /
    "data"
    /
    "processed"
    /
    country
    /
    "load_weather_dataset.csv"
)


df = pd.read_csv(
    data_file,
    parse_dates=["datetime"]
)


df = (
    df
    .sort_values("datetime")
    .reset_index(drop=True)
)



# =======================================
# Calendar features
# =======================================

df["hour"] = df["datetime"].dt.hour

df["day_of_week"] = (
    df["datetime"]
    .dt.dayofweek
)

df["month"] = (
    df["datetime"]
    .dt.month
)

df["is_weekend"] = (
    df["day_of_week"] >= 5
).astype(int)



# =======================================
# Lag features
# =======================================

df["load_lag_1"] = (
    df["load_mwh"]
    .shift(1)
)


df["load_lag_24"] = (
    df["load_mwh"]
    .shift(24)
)


df["load_lag_168"] = (
    df["load_mwh"]
    .shift(168)
)



# Rolling

df["load_mean_24"] = (
    df["load_mwh"]
    .shift(1)
    .rolling(24)
    .mean()
)


df["load_std_24"] = (
    df["load_mwh"]
    .shift(1)
    .rolling(24)
    .std()
)



df = df.dropna()



# =======================================
# Features
# =======================================

features = [

    "temperature_2m",

    "relative_humidity_2m",

    "wind_speed_10m",

    "cloud_cover",

    "surface_pressure",

    "shortwave_radiation",

    "hour",

    "day_of_week",

    "month",

    "is_weekend",

    "load_lag_1",

    "load_lag_24",

    "load_lag_168",

    "load_mean_24",

    "load_std_24"

]



# =======================================
# Load model
# =======================================

model_file = (
    BASE_DIR
    /
    "models"
    /
    country
    /
    "xgboost_load_forecaster.pkl"
)


model = joblib.load(
    model_file
)



# =======================================
# Rolling backtest
# =======================================

results = []


dates = pd.date_range(
    start=start_date,
    end=end_date,
    freq="D"
)


print(
    f"Running backtest: {len(dates)} days"
)



for date in dates:


    day = df[
        df["datetime"].dt.date
        ==
        date.date()
    ]


    if len(day) != 24:
        continue


    X = day[features]

    y = day["load_mwh"]


    prediction = model.predict(
        X
    )


    mae = mean_absolute_error(
        y,
        prediction
    )


    rmse = (
        mean_squared_error(
            y,
            prediction
        )
        **0.5
    )


    r2 = r2_score(
        y,
        prediction
    )


    mape = (
        abs(
            (y - prediction)
            /
            y
        )
        .mean()
        *
        100
    )


    results.append({

        "date": date.date(),

        "MAE": mae,

        "RMSE": rmse,

        "R2": r2,

        "MAPE": mape

    })



results = pd.DataFrame(
    results
)



# =======================================
# Summary
# =======================================

print()

print("==============================")

print("Rolling Backtest Results")

print("==============================")

print()


print(
    results.mean(
        numeric_only=True
    )
)



# =======================================
# Save
# =======================================

output_dir = (
    BASE_DIR
    /
    "reports"
    /
    country
)

output_dir.mkdir(
    parents=True,
    exist_ok=True
)


output_file = (
    output_dir
    /
    "rolling_backtest_results.csv"
)


results.to_csv(
    output_file,
    index=False
)


print()

print(
    f"Saved:\n{output_file}"
)