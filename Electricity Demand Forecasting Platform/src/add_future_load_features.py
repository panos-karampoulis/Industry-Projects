import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

country = "germany"

forecast_date = "2026-07-24"


# ---------------------------------------
# Load future weather features
# ---------------------------------------

future_file = (
    BASE_DIR
    /
    "data"
    /
    "future"
    /
    country
    /
    f"future_weather_features_{forecast_date}.csv"
)


future = pd.read_csv(
    future_file,
    parse_dates=["datetime"]
)


# ---------------------------------------
# Load historical processed dataset
# ---------------------------------------

history_file = (
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


history = pd.read_csv(
    history_file,
    parse_dates=["datetime"]
)


history = (
    history
    .sort_values("datetime")
    .set_index("datetime")
)



# ---------------------------------------
# Create load lag features
# ---------------------------------------

load_series = history["load_mwh"]



future["load_lag_24"] = [
    load_series.get(
        dt - pd.Timedelta(hours=24)
    )
    for dt in future["datetime"]
]


future["load_lag_168"] = [
    load_series.get(
        dt - pd.Timedelta(hours=168)
    )
    for dt in future["datetime"]
]



# ---------------------------------------
# Rolling statistics
# ---------------------------------------

rolling_mean = []

rolling_std = []


for dt in future["datetime"]:

    previous_values = load_series[
        dt - pd.Timedelta(hours=24):
        dt
    ]


    rolling_mean.append(
        previous_values.mean()
    )


    rolling_std.append(
        previous_values.std()
    )



future["load_mean_24"] = rolling_mean

future["load_std_24"] = rolling_std



# ---------------------------------------
# Save final future features
# ---------------------------------------

output_file = (
    BASE_DIR
    /
    "data"
    /
    "future"
    /
    country
    /
    f"final_future_features_{forecast_date}.csv"
)


future.to_csv(
    output_file,
    index=False
)



print(future.head())

print()

print(
    "Dataset shape:",
    future.shape
)

print()

print(
    future.isna().sum()
)

print()

print(
    f"Saved:\n{output_file}"
)