import pandas as pd
from pathlib import Path


# ==========================================================
# CONFIG
# ==========================================================

BASE_DIR = Path(__file__).resolve().parents[2]

RAW_DIR = BASE_DIR / "data" / "raw"


COUNTRIES = [
    "germany",
    "netherlands",
    "france",
    "spain",
    "italy"
]


FILES = [
    "load.csv",
    "day_ahead.csv",
    "generation.csv"
]


# ==========================================================
# CHECK FUNCTIONS
# ==========================================================

def check_dataset(path):

    print("\n")
    print("=" * 70)
    print(path)
    print("=" * 70)


    try:

        df = pd.read_csv(
            path,
            index_col=0
        )


        # Convert index safely
        df.index = pd.to_datetime(
            df.index,
            errors="coerce"
        )


        # Remove invalid timestamps
        df = df[df.index.notna()]


        print("\nShape:")
        print(df.shape)


        print("\nColumns:")
        print(df.columns.tolist())


        print("\nFirst rows:")
        print(df.head())


        print("\nMissing values:")
        print(df.isna().sum())


        print("\nDuplicates:")
        print(
            df.index.duplicated().sum()
        )


        if len(df.index) > 1:

            diff = (
                df.index[1:]
                -
                df.index[:-1]
            )


            print("\nMost common time intervals:")

            print(
                diff.value_counts()
                .head()
            )


        print("\nStart date:")
        print(df.index.min())


        print("\nEnd date:")
        print(df.index.max())


    except Exception as e:

        print(
            f"FAILED: {e}"
        )
# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":


    for country in COUNTRIES:


        folder = RAW_DIR / country


        for file in FILES:


            path = folder / file


            if path.exists():

                check_dataset(
                    path
                )

            else:

                print(
                    f"Missing file: {path}"
                )


    print("\n")
    print("="*70)
    print("DATA QUALITY CHECK COMPLETED")
    print("="*70)