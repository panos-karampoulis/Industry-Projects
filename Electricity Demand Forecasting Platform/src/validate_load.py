import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


country = "germany"


file = (
    BASE_DIR
    /
    "data"
    /
    "raw"
    /
    country
    /
    f"{country}_load.csv"
)


df = pd.read_csv(
    file,
    parse_dates=["datetime"]
)


print("Dataset shape:")
print(df.shape)


print("\nDate range:")
print(
    df["datetime"].min(),
    "to",
    df["datetime"].max()
)


print("\nMissing values:")
print(
    df.isna().sum()
)


print("\nDuplicates:")
print(
    df["datetime"].duplicated().sum()
)


# expected hourly frequency

expected = pd.date_range(
    start=df["datetime"].min(),
    end=df["datetime"].max(),
    freq="h"
)


missing_hours = (
    expected
    .difference(df["datetime"])
)


print("\nMissing timestamps:")
print(
    len(missing_hours)
)


if len(missing_hours) > 0:
    print(missing_hours[:10])


print("\nValidation completed.")