import pandas as pd


BASE = r"D:\Portfolio\Intraday Market Forecasting - updated\data\processed"


countries = [
    "germany",
    "france",
    "italy",
    "netherlands",
    "spain"
]


for c in countries:

    print("\n")
    print("="*50)
    print(c.upper())
    print("="*50)


    file = (
        BASE
        +
        f"\\{c}_intraday_prices.csv"
    )


    df = pd.read_csv(
        file
    )


    print(
        df.tail()
    )


    print("\nResolution:")
    
    print(
        df["resolution"].value_counts()
    )


    print("\nLast timestamp:")

    print(
        df["timestamp"].max()
    )