import pandas as pd
from pathlib import Path


# -------------------------
# Paths
# -------------------------

BASE_DIR = Path(__file__).resolve().parent.parent


RAW_DIR = (
    BASE_DIR
    / "data"
    / "raw"
    / "italy"
)


OUTPUT_DIR = (
    BASE_DIR
    / "data"
    / "processed"
    / "italy"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


OUTPUT_FILE = (
    OUTPUT_DIR
    / "italy_generation.csv"
)



# -------------------------
# Load Excel files
# -------------------------

print("Loading Italy energy data...")


files = sorted(
    RAW_DIR.glob("italy_*.xlsx")
)


if not files:
    raise FileNotFoundError(
        "No Italy Excel files found in data/raw/italy/"
    )


frames = []


for file in files:

    print(
        "Reading:",
        file.name
    )

    df = pd.read_excel(
        file,
        engine="openpyxl"
    )

    frames.append(df)



raw = pd.concat(
    frames,
    ignore_index=True
)


print(
    "Raw shape:",
    raw.shape
)


print(
    raw.columns.tolist()
)



# -------------------------
# Cleaning
# -------------------------

df = raw.copy()


# Convert Date
# removes Terna metadata rows automatically

df["datetime"] = pd.to_datetime(
    df["Date"],
    dayfirst=True,
    errors="coerce"
)


df = df.dropna(
    subset=["datetime"]
)


print(
    "After date cleaning:",
    df.shape
)



# -------------------------
# Generation numeric
# -------------------------

df["generation"] = (
    df["Actual Generation"]
    .astype(str)
    .str.replace(
        ",",
        ".",
        regex=False
    )
)


df["generation"] = pd.to_numeric(
    df["generation"],
    errors="coerce"
)


df = df.dropna(
    subset=["generation"]
)



# -------------------------
# Keep renewable sources
# -------------------------

df = df[
    df["Primary Source"].isin(
        [
            "Photovoltaic",
            "Wind"
        ]
    )
]


print(
    "Renewable rows:",
    df.shape
)


print(
    "Sources:",
    df["Primary Source"].unique()
)



# -------------------------
# Pivot Solar / Wind
# -------------------------

pivot = (
    df
    .pivot_table(
        index="datetime",
        columns="Primary Source",
        values="generation",
        aggfunc="sum"
    )
    .reset_index()
)



# -------------------------
# Rename columns
# -------------------------

pivot = pivot.rename(
    columns={
        "Photovoltaic": "solar_mwh",
        "Wind": "wind_total_mwh"
    }
)



# Missing protection

if "solar_mwh" not in pivot.columns:
    pivot["solar_mwh"] = 0


if "wind_total_mwh" not in pivot.columns:
    pivot["wind_total_mwh"] = 0



# -------------------------
# Final schema before resample
# -------------------------

pivot["country"] = "italy"


pivot["wind_onshore_mwh"] = (
    pivot["wind_total_mwh"]
)


pivot["wind_offshore_mwh"] = 0



final = pivot[
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
# Convert mixed frequency to hourly
# -------------------------
# Terna contains hourly + 15-minute data.
# Values are MW, therefore use mean.


final = (
    final
    .set_index("datetime")
    [
        [
            "solar_mwh",
            "wind_onshore_mwh",
            "wind_offshore_mwh",
            "wind_total_mwh"
        ]
    ]
    .resample("1h")
    .mean()
    .reset_index()
)


final["country"] = "italy"



# Restore country

final["country"] = "italy"



# Remove empty timestamps

final = final.dropna(
    subset=[
        "solar_mwh",
        "wind_total_mwh"
    ]
)



# Sort

final = final.sort_values(
    "datetime"
)



# -------------------------
# Save
# -------------------------

final.to_csv(
    OUTPUT_FILE,
    index=False
)


print()

print(
    "Saved:",
    OUTPUT_FILE
)


print()

print(
    final.head()
)


print()

print(
    "Final shape:",
    final.shape
)