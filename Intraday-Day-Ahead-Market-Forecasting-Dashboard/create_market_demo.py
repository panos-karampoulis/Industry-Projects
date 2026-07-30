import pandas as pd
from pathlib import Path


# ============================================================
# PATHS
# ============================================================

SOURCE = Path(
    "data/processed/europe_intraday_prices.csv"
)


OUTPUT = Path(
    "demo_data/market/europe_intraday_prices.csv"
)


COUNTRIES = [
    "germany",
    "france",
    "italy",
    "netherlands",
    "spain"
]


# ============================================================
# LOAD
# ============================================================

print("Loading dataset...")


df = pd.read_csv(SOURCE)



df["timestamp"] = pd.to_datetime(
    df["timestamp"],
    utc=True
)



print(
    "Original countries:"
)

print(
    df["country"].unique()
)



# ============================================================
# CREATE COMMON TIMELINE
# ============================================================


common_timestamps = (

    df

    .groupby("timestamp")

    .filter(

        lambda x:

        set(COUNTRIES)

        .issubset(

            set(
                x["country"]
            )

        )

    )

    ["timestamp"]

    .drop_duplicates()

    .sort_values()

)



print(
    "Common timestamps:",
    len(common_timestamps)
)



# keep enough rows
common_timestamps = (
    common_timestamps
    .head(5000)
)



# ============================================================
# FILTER DATA
# ============================================================


demo = (

    df

    [

        df["timestamp"]

        .isin(common_timestamps)

    ]

    [

        df["country"]

        .isin(COUNTRIES)

    ]

)



print()


print(
    demo.groupby("country").size()
)



# ============================================================
# SAVE
# ============================================================


OUTPUT.parent.mkdir(
    parents=True,
    exist_ok=True
)



demo.to_csv(
    OUTPUT,
    index=False
)



print()


print(
    "Created:",
    OUTPUT
)


print(
    demo.shape
)