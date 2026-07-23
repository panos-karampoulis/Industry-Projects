import pandas as pd
import joblib

from pathlib import Path

from sklearn.model_selection import train_test_split
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
    parse_dates=["datetime"]
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
    df["datetime"].dt.hour
)


df["day_of_week"] = (
    df["datetime"].dt.dayofweek
)


df["month"] = (
    df["datetime"].dt.month
)


df["week_of_year"] = (
    df["datetime"].dt.isocalendar().week
    .astype(int)
)


df["is_weekend"] = (
    df["day_of_week"] >= 5
).astype(int)



# -----------------------------------
# Load history features
# -----------------------------------

df["load_lag_24"] = (
    df["load_mwh"]
    .shift(24)
)


df["load_lag_168"] = (
    df["load_mwh"]
    .shift(168)
)



df["load_mean_24"] = (

    df["load_mwh"]
    .shift(1)
    .rolling(24)
    .mean()

)



df["load_mean_168"] = (

    df["load_mwh"]
    .shift(1)
    .rolling(168)
    .mean()

)



df["load_mean_720"] = (

    df["load_mwh"]
    .shift(1)
    .rolling(720)
    .mean()

)



df["load_std_24"] = (

    df["load_mwh"]
    .shift(1)
    .rolling(24)
    .std()

)



df = df.dropna()



# -----------------------------------
# Features
# -----------------------------------

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

    "week_of_year",

    "is_weekend",

    "load_lag_24",

    "load_lag_168",

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

    n_estimators=500,

    learning_rate=0.03,

    max_depth=8,

    subsample=0.8,

    colsample_bytree=0.8,

    random_state=42

)



model.fit(
    X_train,
    y_train
)



# -----------------------------------
# Evaluation
# -----------------------------------

prediction = model.predict(
    X_test
)



mae = mean_absolute_error(
    y_test,
    prediction
)


rmse = mean_squared_error(
    y_test,
    prediction
) ** 0.5


r2 = r2_score(
    y_test,
    prediction
)



print("===================")
print("XGBoost v2 Results")
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
# Save model
# -----------------------------------

model_dir = (

    BASE_DIR
    /
    "models"
    /
    country

)


model_dir.mkdir(
    exist_ok=True,
    parents=True
)



model_file = (

    model_dir
    /
    "xgboost_load_forecaster_v2.pkl"

)



joblib.dump(
    model,
    model_file
)



print()

print(
    f"Saved:\n{model_file}"
)