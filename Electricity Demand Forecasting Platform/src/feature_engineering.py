import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


country = "germany"


# ---------------------------------------
# Load dataset
# ---------------------------------------

input_file = (
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


print("Loading dataset...")


df = pd.read_csv(
    input_file,
    parse_dates=["datetime"]
)


df = df.sort_values(
    "datetime"
)



# ---------------------------------------
# Calendar features
# ---------------------------------------

print("Creating calendar features...")


df["hour"] = (
    df["datetime"]
    .dt.hour
)


df["day_of_week"] = (
    df["datetime"]
    .dt.dayofweek
)


df["month"] = (
    df["datetime"]
    .dt.month
)


df["is_weekend"] = (
    df["day_of_week"]
    >= 5
).astype(int)



# ---------------------------------------
# Load lag features
# ---------------------------------------

print("Creating lag features...")


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



# ---------------------------------------
# Rolling statistics
# ---------------------------------------

print("Creating rolling features...")


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



# ---------------------------------------
# Target creation
# ---------------------------------------

print("Creating forecasting target...")


# next hour demand

df["target_load"] = (
    df["load_mwh"]
    .shift(-1)
)



# ---------------------------------------
# Remove missing rows
# ---------------------------------------

df = df.dropna()



# ---------------------------------------
# Save features
# ---------------------------------------

output_file = (
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


df.to_csv(
    output_file,
    index=False
)


print()

print("Feature dataset shape:")
print(df.shape)


print()

print(
    f"Saved to:\n{output_file}"
)