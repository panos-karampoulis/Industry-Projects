import pandas as pd
import joblib

from pathlib import Path

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

from xgboost import XGBRegressor



BASE_DIR = Path(__file__).resolve().parent.parent


country = "germany"



# -----------------------------------
# Load dataset
# -----------------------------------

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

    parse_dates=[
        "datetime"
    ]

)



df = (

    df
    .sort_values("datetime")
    .reset_index(drop=True)

)



# -----------------------------------
# Calendar features
# -----------------------------------

df["hour"] = (
    df.datetime.dt.hour
)


df["day_of_week"] = (
    df.datetime.dt.dayofweek
)


df["month"] = (
    df.datetime.dt.month
)


df["day_of_year"] = (
    df.datetime.dt.dayofyear
)


df["week_of_year"] = (

    df.datetime
    .dt.isocalendar()
    .week
    .astype(int)

)


df["is_weekend"] = (

    df.day_of_week >= 5

).astype(int)



# -----------------------------------
# Cyclic features
# -----------------------------------

import numpy as np


df["hour_sin"] = (

    np.sin(
        2*np.pi*df["hour"]/24
    )

)


df["hour_cos"] = (

    np.cos(
        2*np.pi*df["hour"]/24
    )

)



df["day_year_sin"] = (

    np.sin(
        2*np.pi*df["day_of_year"]/365
    )

)



df["day_year_cos"] = (

    np.cos(
        2*np.pi*df["day_of_year"]/365
    )

)



# -----------------------------------
# Load history features
# -----------------------------------

df["load_lag_24"] = (

    df.load_mwh
    .shift(24)

)


df["load_lag_168"] = (

    df.load_mwh
    .shift(168)

)



# same hour previous year

df["load_lag_8760"] = (

    df.load_mwh
    .shift(8760)

)



df["load_mean_24"] = (

    df.load_mwh
    .shift(1)
    .rolling(24)
    .mean()

)



df["load_mean_168"] = (

    df.load_mwh
    .shift(1)
    .rolling(168)
    .mean()

)



df["load_mean_720"] = (

    df.load_mwh
    .shift(1)
    .rolling(720)
    .mean()

)



df["load_std_24"] = (

    df.load_mwh
    .shift(1)
    .rolling(24)
    .std()

)



df = df.dropna()



# -----------------------------------
# Features
# -----------------------------------

features = [

    # weather

    "temperature_2m",

    "relative_humidity_2m",

    "wind_speed_10m",

    "cloud_cover",

    "surface_pressure",

    "shortwave_radiation",



    # calendar

    "hour",

    "day_of_week",

    "month",

    "day_of_year",

    "week_of_year",

    "is_weekend",


    # cyclic

    "hour_sin",

    "hour_cos",

    "day_year_sin",

    "day_year_cos",



    # demand history

    "load_lag_24",

    "load_lag_168",

    "load_lag_8760",

    "load_mean_24",

    "load_mean_168",

    "load_mean_720",

    "load_std_24"

]



X = df[features]

y = df["load_mwh"]



# -----------------------------------
# Time split
# -----------------------------------

split = int(
    len(df)*0.8
)


X_train = X.iloc[:split]

X_test = X.iloc[split:]


y_train = y.iloc[:split]

y_test = y.iloc[split:]



# -----------------------------------
# Model
# -----------------------------------

model = XGBRegressor(

    n_estimators=700,

    learning_rate=0.03,

    max_depth=8,

    subsample=0.85,

    colsample_bytree=0.85,

    random_state=42

)



model.fit(

    X_train,

    y_train

)



# -----------------------------------
# Evaluation
# -----------------------------------

pred = model.predict(
    X_test
)



mae = mean_absolute_error(
    y_test,
    pred
)


rmse = (

    mean_squared_error(
        y_test,
        pred
    )
    **0.5

)


r2 = r2_score(
    y_test,
    pred
)



print("===================")
print("XGBoost v3 Results")
print("===================")

print()

print(
    f"MAE: {mae:.2f} MW"
)

print(
    f"RMSE: {rmse:.2f} MW"
)

print(
    f"R2: {r2:.4f}"
)



# -----------------------------------
# Save
# -----------------------------------

model_dir = (

    BASE_DIR
    /
    "models"
    /
    country

)


model_dir.mkdir(
    parents=True,
    exist_ok=True
)



model_file = (

    model_dir
    /
    "xgboost_load_forecaster_v3.pkl"

)



joblib.dump(

    model,

    model_file

)



print()

print(
    f"Saved:\n{model_file}"
)