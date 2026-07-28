import pandas as pd
import numpy as np
import xml.etree.ElementTree as ET
from pathlib import Path


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(
    r"D:\Portfolio\Intraday Market Forecasting - updated"
)

RAW_INTRADAY = (
    BASE_DIR /
    "data" /
    "raw" /
    "intraday_history"
)

RAW_WEATHER = (
    BASE_DIR /
    "data" /
    "raw" /
    "weather"
)

OUTPUT_DIR = (
    BASE_DIR /
    "data" /
    "processed"
)

OUTPUT_FILE = (
    OUTPUT_DIR /
    "europe_intraday_weather_features.csv"
)


COUNTRIES = [
    "germany",
    "france",
    "italy",
    "netherlands",
    "spain"
]


# ============================================================
# XML PARSER (namespace independent)
# ============================================================

def clean_namespace(root):

    for elem in root.iter():

        if "}" in elem.tag:
            elem.tag = elem.tag.split("}", 1)[1]


    return root



def parse_intraday_xml(
        file_path,
        country
):

    rows = []


    print(
        f"Reading {file_path.name}"
    )


    tree = ET.parse(
        file_path
    )

    root = tree.getroot()


    root = clean_namespace(
        root
    )


    periods = root.findall(
        ".//Period"
    )


    for period in periods:


        resolution = period.find(
            "resolution"
        )


        if resolution is None:
            continue


        if resolution.text == "PT15M":

            minutes_step = 15


        elif resolution.text == "PT30M":

            minutes_step = 30


        elif resolution.text == "PT60M":

            minutes_step = 60


        else:

            continue



        start = period.find(
            "./timeInterval/start"
        )


        if start is None:

            continue



        start_time = pd.to_datetime(
            start.text,
            utc=True
        )



        points = period.findall(
            ".//Point"
        )


        for point in points:


            position = point.find(
                "position"
            )


            price = point.find(
                "price.amount"
            )


            if price is None:

                price = point.find(
                    "price"
                )


            if price is None:

                price = point.find(
                    "quantity"
                )



            if position is None or price is None:

                continue



            timestamp = (
                start_time
                +
                pd.Timedelta(
                    minutes=
                    minutes_step *
                    (
                        int(position.text)-1
                    )
                )
            )


            rows.append(
                {
                    "timestamp": timestamp,
                    "country": country,
                    "price_eur_mwh": float(
                        price.text
                    )
                }
            )



    df = pd.DataFrame(
        rows
    )


    return df



# ============================================================
# LOAD INTRADAY HISTORY
# ============================================================

def load_intraday_history(
        country
):


    print(
        f"Loading processed intraday data: {country}"
    )


    file_path = (
        BASE_DIR
        /
        "data"
        /
        "processed"
        /
        f"{country}_intraday_prices.csv"
    )


    if not file_path.exists():

        raise FileNotFoundError(
            f"Missing intraday file: {file_path}"
        )


    df = pd.read_csv(
        file_path
    )


    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        utc=True
    )


    df = df.sort_values(
        "timestamp"
    )


    print(
        "Intraday rows:",
        len(df)
    )


    return df

# ============================================================
# WEATHER
# ============================================================

def load_weather(
        country
):


    file = (
        RAW_WEATHER /
        f"{country}_weather.csv"
    )


    df = pd.read_csv(
        file
    )


    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        utc=True
    )


    return (
        df
        .sort_values(
            "timestamp"
        )
    )



# ============================================================
# FEATURES
# ============================================================

def create_features(
        df
):


    df = df.sort_values(
        "timestamp"
    )


    df["hour"] = (
        df.timestamp.dt.hour
    )


    df["day_of_week"] = (
        df.timestamp.dt.dayofweek
    )


    df["month"] = (
        df.timestamp.dt.month
    )


    df["year"] = (
        df.timestamp.dt.year
    )


    df["weekend"] = (
        df.day_of_week >= 5
    ).astype(int)



    df["is_peak"] = (
        df.hour.between(
            8,
            20
        )
    ).astype(int)


    df["is_off_peak"] = (
        1 -
        df["is_peak"]
    )


    df["night_period"] = (
        df.hour.between(
            0,
            6
        )
    ).astype(int)


    df["morning_ramp"] = (
        df.hour.between(
            6,
            9
        )
    ).astype(int)


    df["evening_peak"] = (
        df.hour.between(
            17,
            21
        )
    ).astype(int)



    # LAGS

    df["lag_1"] = (
        df.price_eur_mwh.shift(1)
    )


    df["lag_4"] = (
        df.price_eur_mwh.shift(4)
    )


    df["lag_96"] = (
        df.price_eur_mwh.shift(96)
    )


    df["lag_672"] = (
        df.price_eur_mwh.shift(672)
    )



    # ROLLING


    df["rolling_mean_96"] = (
        df.price_eur_mwh
        .rolling(96)
        .mean()
    )


    df["rolling_std_96"] = (
        df.price_eur_mwh
        .rolling(96)
        .std()
    )


    df["rolling_mean_672"] = (
        df.price_eur_mwh
        .rolling(672)
        .mean()
    )


    return df



# ============================================================
# MAIN
# ============================================================


def main():


    OUTPUT_DIR.mkdir(
        exist_ok=True
    )


    datasets = []


    for country in COUNTRIES:


        print("\n")
        print("="*60)
        print(country.upper())
        print("="*60)



        intraday = load_intraday_history(
            country
        )


        print(
            "Intraday rows:",
            len(intraday)
        )



        if intraday.empty:

            continue



        weather = load_weather(
            country
        )


        print(
            "Weather rows:",
            len(weather)
        )



        df = pd.merge_asof(
            intraday.sort_values(
                "timestamp"
            ),
            weather.sort_values(
                "timestamp"
            ),
            on="timestamp",
            direction="nearest"
        )



        print(
            "After merge:",
            len(df)
        )



        weather_cols = [
            c for c in weather.columns
            if c!="timestamp"
        ]



        for col in weather_cols:

            if col in df.columns:

                df[col] = (
                    df[col]
                    .ffill()
                    .bfill()
                )



        df = create_features(
            df
        )


        df["country"] = country


        df = df.dropna()



        print(
            "Final rows:",
            len(df)
        )



        datasets.append(
            df
        )



    final = pd.concat(
        datasets,
        ignore_index=True
    )



    final = final.sort_values(
        [
            "country",
            "timestamp"
        ]
    )



    final.to_csv(
        OUTPUT_FILE,
        index=False
    )



    print("\n")
    print("="*60)
    print("FINAL DATASET")
    print("="*60)



    print(
        final.groupby(
            "country"
        )
        ["timestamp"]
        .agg(
            [
                "min",
                "max",
                "count"
            ]
        )
    )



    print("\nSaved:")
    print(
        OUTPUT_FILE
    )



if __name__ == "__main__":

    main()