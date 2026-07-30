import pandas as pd

files = [
    "data/raw/germany/prices.csv",
    "data/raw/germany/load.csv",
    "data/raw/germany/generation.csv"
]

for file in files:

    print("\n" + "="*60)
    print(file)

    df = pd.read_csv(file)

    print("\nHEAD:")
    print(df.head())

    print("\nTAIL:")
    print(df.tail())

    print("\nSHAPE:")
    print(df.shape)

    print("\nCOLUMNS:")
    print(df.columns.tolist())