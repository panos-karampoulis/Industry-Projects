import os
import glob
import pandas as pd

# ==========================================================
# CONFIG
# ==========================================================

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

FILE_TYPES = [
    "load",
    "day_ahead",
    "generation"
]


# ==========================================================
# REPAIR FUNCTION
# ==========================================================

def repair_country(country, file_type):

    folder = os.path.join(
        RAW_DIR,
        country
    )

    pattern = os.path.join(
        folder,
        f"{file_type}_20*.csv"
    )

    yearly_files = sorted(
        glob.glob(pattern)
    )

    if len(yearly_files) == 0:

        print(f"{country} {file_type}: no yearly files")

        return

    print("\n")
    print("=" * 70)
    print(country.upper(), file_type.upper())
    print("=" * 70)

    frames = []

    for file in yearly_files:

        print(
            "Reading:",
            os.path.basename(file)
        )

        df = pd.read_csv(
            file,
            low_memory=False
        )

        ts_col = df.columns[0]

        df[ts_col] = pd.to_datetime(
            df[ts_col],
            utc=True,
            errors="coerce"
        )

        # Remove invalid timestamps
        df = df.dropna(subset=[ts_col])

        frames.append(df)

    merged = pd.concat(
        frames,
        ignore_index=True
    )

    before = len(merged)

    ts_col = merged.columns[0]

    merged = merged.dropna(subset=[ts_col])

    merged = merged.drop_duplicates(
        subset=ts_col,
        keep="last"
    )

    merged = merged.sort_values(
        ts_col
    )

    merged = merged.reset_index(
        drop=True
    )

    after = len(merged)

    output = os.path.join(
        folder,
        f"{file_type}.csv"
    )

    merged.to_csv(
        output,
        index=False
    )

    print()
    print("Saved:", output)
    print("Rows before :", before)
    print("Rows after  :", after)
    print("Duplicates removed :", before - after)
    print("First :", merged.iloc[0][ts_col])
    print("Last  :", merged.iloc[-1][ts_col])


# ==========================================================
# MAIN
# ==========================================================

print("=" * 80)
print("REPAIRING HISTORICAL DATASETS")
print("=" * 80)

for country in COUNTRIES:

    for file_type in FILE_TYPES:

        repair_country(
            country,
            file_type
        )

print("\n")
print("=" * 80)
print("ALL HISTORICAL FILES REPAIRED")
print("=" * 80)