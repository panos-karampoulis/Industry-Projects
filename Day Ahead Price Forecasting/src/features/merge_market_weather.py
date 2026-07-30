import pandas as pd
from pathlib import Path
import argparse


# ============================================================
# Paths
# ============================================================

BASE_PATH = Path("data")


# ============================================================
# Fix datetime index
# ============================================================

def fix_datetime_index(df):

    # Convert mixed timezone timestamps safely
    df.index = pd.to_datetime(
        df.index,
        errors="coerce",
        utc=True
    )


    # remove invalid timestamps
    df = df[~df.index.isna()]


    # Convert UTC -> Germany local time
    df.index = (
        df.index
        .tz_convert(
            "Europe/Berlin"
        )
    )


    # remove duplicates
    df = df[
        ~df.index.duplicated(
            keep="first"
        )
    ]


    return df



# ============================================================
# Load market features
# ============================================================

def load_market(
        country,
        year,
        month
):

    path = (
        BASE_PATH
        /
        "features"
        /
        country.lower()
        /
        str(year)
        /
        f"{month:02d}"
        /
        "features_dataset.csv"
    )


    print()
    print("Loading market dataset...")
    print(path)


    df = pd.read_csv(
        path,
        index_col="datetime"
    )


    df = fix_datetime_index(df)


    print(df.shape)


    return df



# ============================================================
# Load weather
# ============================================================

def load_weather(
        country,
        year,
        month
):

    path = (
        BASE_PATH
        /
        "raw"
        /
        "weather"
        /
        country.lower()
        /
        str(year)
        /
        f"{month:02d}"
        /
        "weather.csv"
    )


    print()
    print("Loading weather dataset...")
    print(path)


    df = pd.read_csv(
        path
    )


    # Convert datetime
    df["datetime"] = pd.to_datetime(
        df["datetime"],
        errors="coerce"
    )


    df = df[
        ~df["datetime"].isna()
    ]


    df = df.set_index(
        "datetime"
    )


    # Weather data is already local hourly data
    # Keep timezone naive to avoid DST ambiguity

    df.index = (
        pd.DatetimeIndex(df.index)
    )


    # Remove duplicates
    df = df[
        ~df.index.duplicated(
            keep="first"
        )
    ]


    return df
# ============================================================
# Merge
# ============================================================

def merge_market_weather(
        country,
        year,
        month
):


    market = load_market(
        country,
        year,
        month
    )


    weather = load_weather(
        country,
        year,
        month
    )




    # Normalize datetime indexes before merging

    # Market: remove timezone
    if market.index.tz is not None:
        market.index = market.index.tz_localize(None)


    # Weather: already timezone naive
    weather.index = pd.DatetimeIndex(
        weather.index
    )

    print()
    print("Merging...")


    

    final = (
        market
        .join(
            weather,
            how="left"
        )
    )


    print()
    print("Final dataset:")
    print(final.head())


    print()
    print(final.shape)


    print()
    print("Missing values:")
    print(
        final.isna()
        .sum()
        .sum()
    )


    output_path = (
        BASE_PATH
        /
        "final"
        /
        country.lower()
        /
        str(year)
        /
        f"{month:02d}"
    )


    output_path.mkdir(
        parents=True,
        exist_ok=True
    )


    output_file = (
        output_path
        /
        "day_ahead_dataset.csv"
    )


    final.to_csv(
        output_file
    )


    print()
    print("Saved:")
    print(output_file)



# ============================================================
# Main
# ============================================================

def main():


    parser = argparse.ArgumentParser()


    parser.add_argument(
        "--country",
        required=True
    )


    parser.add_argument(
        "--year",
        type=int,
        required=True
    )


    parser.add_argument(
        "--month",
        type=int,
        required=True
    )


    args = parser.parse_args()



    print("="*60)
    print("Merging Market + Weather Dataset")
    print("="*60)

    print(
        f"Country: {args.country.lower()}"
    )

    print(
        f"Period: {args.year}-{args.month:02d}"
    )


    merge_market_weather(
        args.country,
        args.year,
        args.month
    )



if __name__ == "__main__":
    main()