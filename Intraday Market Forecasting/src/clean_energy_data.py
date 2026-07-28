import pandas as pd
from pathlib import Path


# ==========================================================
# CONFIG
# ==========================================================

BASE_DIR = Path(__file__).resolve().parents[2]

RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"


COUNTRIES = [
    "germany",
    "netherlands",
    "france",
    "spain",
    "italy"
]


# ==========================================================
# HELPERS
# ==========================================================

def load_csv(path):

    df = pd.read_csv(
        path,
        index_col=0
    )

    # Convert timestamps safely
    df.index = pd.to_datetime(
        df.index,
        utc=True,
        errors="coerce"
    )

    # Remove invalid timestamps
    df = df[df.index.notna()]

    # Sort
    df = df.sort_index()

    # Remove duplicates
    df = df[~df.index.duplicated(
        keep="first"
    )]

    return df



def clean_generation(df):

    # Remove empty metadata rows
    df = df[df.index.notna()]

    # Convert columns to numeric
    for col in df.columns:

        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )

    # Missing values
    df = df.fillna(0)

    return df



def add_time_features(df):

    df["hour"] = df.index.hour

    df["day_of_week"] = (
        df.index.dayofweek
    )

    df["month"] = (
        df.index.month
    )


    df["weekend"] = (
        df.index.dayofweek >= 5
    ).astype(int)


    def season(month):

        if month in [12,1,2]:
            return "winter"

        elif month in [3,4,5]:
            return "spring"

        elif month in [6,7,8]:
            return "summer"

        else:
            return "autumn"


    df["season"] = (
        df["month"]
        .apply(season)
    )


    return df



# ==========================================================
# COUNTRY PROCESSING
# ==========================================================

def process_country(country):


    print("\n")
    print("="*70)
    print(country.upper())
    print("="*70)


    folder = RAW_DIR / country


    load_file = folder / "load.csv"
    price_file = folder / "day_ahead.csv"
    generation_file = folder / "generation.csv"


    dataframes = []


    # -------------------------
    # LOAD
    # -------------------------

    if load_file.exists():

        print("Loading load...")

        load = load_csv(
            load_file
        )

        load.columns = [
            "load_mw"
        ]

        dataframes.append(
            load
        )


    # -------------------------
    # DAY AHEAD PRICE
    # -------------------------

    if price_file.exists():

        print("Loading price...")

        price = load_csv(
            price_file
        )

        price.columns = [
            "price_eur_mwh"
        ]


        # hourly -> 15 min
        price = price.resample(
            "15min"
        ).ffill()


        dataframes.append(
            price
        )



    # -------------------------
    # GENERATION
    # -------------------------

    if generation_file.exists():

        print("Loading generation...")

        generation = load_csv(
            generation_file
        )


        generation = clean_generation(
            generation
        )


        # keep only useful renewables
        selected = []


        for col in generation.columns:

            name = col.lower()

            if (
                "wind" in name
                or
                "solar" in name
                or
                "hydro" in name
            ):

                selected.append(col)


        if len(selected) > 0:

            generation = generation[
                selected
            ]


        dataframes.append(
            generation
        )



    # -------------------------
    # MERGE
    # -------------------------

    if len(dataframes)==0:

        print(
            "No data found"
        )

        return



    print(
        "Merging datasets..."
    )


    df = pd.concat(
        dataframes,
        axis=1
    )


    # 15 min frequency
    df = df.resample(
        "15min"
    ).mean()


    # Missing values
    df = df.interpolate(
        method="time"
    )


    # Time features
    df = add_time_features(
        df
    )


    output = (
        PROCESSED_DIR /
        f"{country}_clean.csv"
    )


    PROCESSED_DIR.mkdir(
        exist_ok=True
    )


    df.to_csv(
        output
    )


    print(
        f"Saved: {output}"
    )


    print(
        df.shape
    )



# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":


    for country in COUNTRIES:

        process_country(
            country
        )


    print("\n")
    print("="*70)
    print("PREPROCESSING COMPLETED")
    print("="*70)