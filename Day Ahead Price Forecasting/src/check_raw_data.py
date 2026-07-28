from pathlib import Path
import pandas as pd


base = Path(
    "data/raw/germany/2020/01"
)


for file in base.glob("*.csv"):

    print("\n")
    print("="*50)
    print(file.name)

    df = pd.read_csv(
        file
    )

    print(df.head())

    print("\nShape:")
    print(df.shape)

    print("\nMissing:")
    print(df.isna().sum().sum())