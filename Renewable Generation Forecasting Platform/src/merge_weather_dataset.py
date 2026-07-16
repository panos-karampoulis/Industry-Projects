import pandas as pd
import argparse
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


parser = argparse.ArgumentParser()

parser.add_argument(
    "--country",
    default="germany"
)

args = parser.parse_args()

COUNTRY = args.country.lower()


# -----------------------
# Paths
# -----------------------

generation_file = (
    BASE_DIR
    /
    "data"
    /
    "processed"
    /
    COUNTRY
    /
    f"{COUNTRY}_generation.csv"
)


weather_file = (
    BASE_DIR
    /
    "data"
    /
    "weather"
    /
    COUNTRY
    /
    "weather.csv"
)



print("Loading generation...")
generation = pd.read_csv(
    generation_file,
    parse_dates=["datetime"]
)


print(
    generation.shape
)



print("Loading weather...")

weather = pd.read_csv(
    weather_file,
    parse_dates=["datetime"]
)


print(
    weather.shape
)



# -----------------------
# Merge
# -----------------------

df = pd.merge(
    generation,
    weather,
    on="datetime",
    how="inner"
)



df = (
    df
    .sort_values("datetime")
    .reset_index(drop=True)
)



print()
print("Merged dataset:")
print(df.head())

print()
print(
    "Shape:",
    df.shape
)



# -----------------------
# Save
# -----------------------

output = (
    BASE_DIR
    /
    "data"
    /
    "processed"
    /
    COUNTRY
    /
    "merged_generation_weather.csv"
)


df.to_csv(
    output,
    index=False
)


print()
print("Saved:")
print(output)