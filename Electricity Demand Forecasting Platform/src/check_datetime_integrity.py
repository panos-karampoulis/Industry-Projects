import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


file = (
    BASE_DIR
    /
    "data"
    /
    "processed"
    /
    "germany"
    /
    "load_weather_dataset.csv"
)


df = pd.read_csv(
    file,
    parse_dates=["datetime"]
)


df = df.sort_values("datetime")


print("Dataset range:")
print(df.datetime.min())
print(df.datetime.max())


print()

print("Rows per day:")

daily = (
    df
    .groupby(
        df["datetime"].dt.date
    )
    .size()
)


print(
    daily.tail(10)
)


print()

print("Days with missing hours:")

print(
    daily[daily != 24]
)