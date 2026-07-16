import pandas as pd
import requests
from pathlib import Path


# -------------------------
# Paths
# -------------------------

BASE_DIR = Path(__file__).resolve().parent.parent


OUTPUT_DIR = (
    BASE_DIR
    /
    "data"
    /
    "processed"
    /
    "denmark"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


OUTPUT_FILE = (
    OUTPUT_DIR
    /
    "denmark_generation.csv"
)


# -------------------------
# Energinet API
# -------------------------

URL = (
    "https://api.energidataservice.dk/dataset/"
    "ProductionConsumptionSettlement"
    "?start=2020-01-01"
    "&end=2025-12-31"
    "&filter=%7B%22PriceArea%22:%22DK1%22%7D"
    "&limit=50000"
)


print("Downloading Denmark energy data...")


response = requests.get(
    URL
)


response.raise_for_status()


data = response.json()



# -------------------------
# Convert JSON to dataframe
# -------------------------

df = pd.DataFrame(
    data["records"]
)


print(
    "Raw shape:",
    df.shape
)


print(
    df.columns.tolist()
)



# -------------------------
# Datetime
# -------------------------

df["datetime"] = pd.to_datetime(
    df["HourDK"]
)



# -------------------------
# Select generation columns
# -------------------------

# -------------------------
# Create renewable columns
# -------------------------


# Solar total

df["solar_mwh"] = (
    df["SolarPowerLt10kW_MWh"].fillna(0)
    +
    df["SolarPowerGe10Lt40kW_MWh"].fillna(0)
    +
    df["SolarPowerGe40kW_MWh"].fillna(0)
    +
    df["SolarPowerSelfConMWh"].fillna(0)
)



# Wind onshore

df["wind_onshore_mwh"] = (
    df["OnshoreWindLt50kW_MWh"].fillna(0)
    +
    df["OnshoreWindGe50kW_MWh"].fillna(0)
)



# Wind offshore

df["wind_offshore_mwh"] = (
    df["OffshoreWindLt100MW_MWh"].fillna(0)
    +
    df["OffshoreWindGe100MW_MWh"].fillna(0)
)



# Total wind

df["wind_total_mwh"] = (
    df["wind_onshore_mwh"]
    +
    df["wind_offshore_mwh"]
)



# Country

df["country"] = "denmark"



# Keep final schema

df = df[
    [
        "datetime",
        "country",
        "solar_mwh",
        "wind_onshore_mwh",
        "wind_offshore_mwh",
        "wind_total_mwh"
    ]
]


# -------------------------
# Cleaning
# -------------------------

df = (
    df
    .sort_values("datetime")
    .drop_duplicates("datetime")
    .reset_index(drop=True)
)



# -------------------------
# Save
# -------------------------

df.to_csv(
    OUTPUT_FILE,
    index=False
)


print()
print("Denmark dataset created successfully")
print("-------------------------------")
print(
    df.shape
)

print()
print(
    OUTPUT_FILE
)

print()
print(
    df.head()
)