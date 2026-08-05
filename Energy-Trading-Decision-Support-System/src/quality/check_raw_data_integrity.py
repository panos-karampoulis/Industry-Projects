import os
import pandas as pd

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

RAW_DIR = os.path.join(
    BASE_DIR,
    "data",
    "raw"
)

COUNTRIES = [
    "germany",
    "france",
    "italy",
    "spain",
    "netherlands"
]

FILES = [
    "load.csv",
    "day_ahead.csv",
    "generation.csv"
]

print("=" * 80)
print("RAW DATA INTEGRITY REPORT")
print("=" * 80)

for country in COUNTRIES:

    print(f"\n{country.upper()}")

    for file in FILES:

        path = os.path.join(
            RAW_DIR,
            country,
            file
        )

        if not os.path.exists(path):

            print(f"{file}: NOT FOUND")
            continue

        df = pd.read_csv(path)

        first = pd.to_datetime(df.iloc[0, 0])
        last = pd.to_datetime(df.iloc[-1, 0])

        duplicates = df.iloc[:, 0].duplicated().sum()

        print(
            f"""
{file}
--------------------------
Rows        : {len(df)}
First       : {first}
Last        : {last}
Duplicates  : {duplicates}
"""
        )
        