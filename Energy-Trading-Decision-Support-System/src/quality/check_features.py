import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]


FEATURE_DIR = (
    BASE_DIR
    /
    "data"
    /
    "features"
)



files = list(
    FEATURE_DIR.glob(
        "*.csv"
    )
)



print("="*70)
print("FEATURE DATA QUALITY CHECK")
print("="*70)



for file in files:


    print("\n")
    print("="*50)
    print(file.name)
    print("="*50)



    df = pd.read_csv(
        file,
        index_col=0,
        parse_dates=True
    )



    print(
        "Shape:",
        df.shape
    )


    print(
        "\nColumns:"
    )

    print(
        list(df.columns)
    )


    print(
        "\nMissing values:",
        df.isna().sum().sum()
    )


    print(
        "Duplicate timestamps:",
        df.index.duplicated().sum()
    )


    print(
        "\nPreview:"
    )

    print(
        df.head()
    )



print("\n")
print("="*70)
print("FEATURE CHECK COMPLETED")
print("="*70)