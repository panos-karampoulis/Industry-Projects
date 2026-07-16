import pandas as pd
from pathlib import Path


# ===============================
# Paths
# ===============================

RAW = Path("data/raw")
PROCESSED = Path("data/processed")


WEATHER_FILE = RAW / "germany_weather.csv"

SMARD_FOLDER = RAW / "smard_generation"


OUTPUT = PROCESSED / "renewable_forecasting_dataset.csv"



# ===============================
# Load weather
# ===============================

print("Loading weather...")

weather = pd.read_csv(
    WEATHER_FILE
)

weather["datetime"] = pd.to_datetime(
    weather["time"]
)

weather.drop(
    columns=["time"],
    inplace=True
)

weather = weather.sort_values(
    "datetime"
)

print(weather.head())
print(weather.shape)


# ===============================
# Load generation
# ===============================

print("Loading solar...")

solar = pd.read_csv(
    SMARD_FOLDER / "solar.csv"
)


solar["datetime"] = pd.to_datetime(
    solar["datetime"]
)



solar = solar.rename(
    columns={
        "solar": "solar_mwh"
    }
)



print("Loading wind onshore...")


wind_onshore = pd.read_csv(
    SMARD_FOLDER / "wind_onshore.csv"
)


wind_onshore["datetime"] = pd.to_datetime(
    wind_onshore["datetime"]
)


wind_onshore = wind_onshore.rename(
    columns={
        "wind_onshore": "wind_onshore_mwh"
    }
)




print("Loading wind offshore...")


wind_offshore = pd.read_csv(
    SMARD_FOLDER / "wind_offshore.csv"
)


wind_offshore["datetime"] = pd.to_datetime(
    wind_offshore["datetime"]
)


wind_offshore = wind_offshore.rename(
    columns={
        "wind_offshore": "wind_offshore_mwh"
    }
)



# ===============================
# Merge generation
# ===============================


generation = solar.merge(
    wind_onshore,
    on="datetime",
    how="outer"
)


generation = generation.merge(
    wind_offshore,
    on="datetime",
    how="outer"
)



generation["wind_total_mwh"] = (
    generation["wind_onshore_mwh"]
    +
    generation["wind_offshore_mwh"]
)



# ===============================
# Merge Weather + Generation
# ===============================


print("Merging datasets...")


df = weather.merge(
    generation,
    on="datetime",
    how="inner"
)



# ===============================
# Cleaning
# ===============================

df = df.sort_values(
    "datetime"
)


df = df.drop_duplicates(
    "datetime"
)


df = df.reset_index(
    drop=True
)



# ===============================
# Save
# ===============================


PROCESSED.mkdir(
    exist_ok=True
)


df.to_csv(
    OUTPUT,
    index=False
)


print()
print("Dataset created:")
print(OUTPUT)

print()

print(df.head())

print()

print(df.shape)

print()

print(df.isna().sum())