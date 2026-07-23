import pandas as pd
import joblib

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


country = "germany"


# ---------------------------------------
# Forecast date
# ---------------------------------------

forecast_date = "2025-12-31"



# ---------------------------------------
# Load processed data
# ---------------------------------------

features_file = (
    BASE_DIR
    /
    "data"
    /
    "processed"
    /
    country
    /
    "load_features.csv"
)


df = pd.read_csv(
    features_file,
    parse_dates=["datetime"]
)


df = df.sort_values(
    "datetime"
)



# ---------------------------------------
# Select forecast day
# ---------------------------------------

forecast = df[
    df["datetime"].dt.date ==
    pd.to_datetime(forecast_date).date()
].copy()



if len(forecast) == 0:

    raise ValueError(
        "Forecast date not available in dataset"
    )



# ---------------------------------------
# Load model
# ---------------------------------------

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



# ---------------------------------------
# Features
# ---------------------------------------

drop_columns = [

    "datetime",

    "target_load",

    "load_mwh"

]


features = [

    col for col in forecast.columns

    if col not in drop_columns

]



X_future = forecast[features]



# ---------------------------------------
# Forecast
# ---------------------------------------

forecast["forecast_load_mw"] = (
    model.predict(
        X_future
    )
)



# ---------------------------------------
# Output
# ---------------------------------------

output = forecast[
    [
        "datetime",
        "forecast_load_mw"
    ]
]


output_dir = (
    BASE_DIR
    /
    "reports"
    /
    country
    /
    "forecasts"
)


output_dir.mkdir(
    parents=True,
    exist_ok=True
)


output_file = (
    output_dir
    /
    f"{country}_load_forecast_{forecast_date}.csv"
)


output.to_csv(
    output_file,
    index=False
)



# ---------------------------------------
# Summary
# ---------------------------------------

print()

print("Forecast rows:")

print(len(output))


if len(output) != 24:

    print(
        "Warning: Forecast does not contain 24 hours"
    )


average_load = (
    output["forecast_load_mw"]
    .mean()
)


peak_value = (
    output["forecast_load_mw"]
    .max()
)


peak_hour = (
    output
    .loc[
        output["forecast_load_mw"].idxmax(),
        "datetime"
    ]
)



daily_energy = (
    output["forecast_load_mw"]
    .sum()
)



print()

print("==============================")

print("Electricity Demand Forecast")

print("==============================")

print()

print(
    f"Country: {country}"
)

print(
    f"Date: {forecast_date}"
)


print()

print(
    f"Average load: {average_load:,.0f} MW"
)


print(
    f"Peak load: {peak_value:,.0f} MW"
)


print(
    f"Peak hour: {peak_hour}"
)


print(
    f"Daily energy: {daily_energy/1000:,.2f} GWh"
)

print()


print(
    f"Saved:\n{output_file}"
)