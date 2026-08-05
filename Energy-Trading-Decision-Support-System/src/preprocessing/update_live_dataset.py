from pathlib import Path
import pandas as pd


# ==========================================================
# PATHS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parents[2]


PROCESSED_DIR = (
    BASE_DIR
    /
    "data"
    /
    "processed"
)


RAW_LATEST_DIR = (
    BASE_DIR
    /
    "data"
    /
    "raw"
    /
    "latest"
)



COUNTRIES = [
    "germany",
    "netherlands",
    "france",
    "spain",
    "italy"
]



# ==========================================================
# UPDATE FUNCTION
# ==========================================================

def update_country(country):


    print("\n")
    print("="*70)
    print(country.upper())
    print("="*70)



    clean_file = (
        PROCESSED_DIR
        /
        f"{country}_clean.csv"
    )



    if not clean_file.exists():

        print(
            "Missing clean dataset:",
            clean_file
        )

        return



    # ------------------------------------------------------
    # Historical dataset
    # ------------------------------------------------------

    historical = pd.read_csv(
        clean_file,
        parse_dates=[
            "timestamp"
        ]
    )


    historical["timestamp"] = pd.to_datetime(
        historical["timestamp"],
        utc=True
    )



    last_timestamp = (
        historical["timestamp"]
        .max()
    )


    print(
        "Current dataset:",
        historical.shape
    )


    print(
        "Last timestamp:",
        last_timestamp
    )



    # ------------------------------------------------------
    # Latest raw data
    # ------------------------------------------------------

    price_file = (
        RAW_LATEST_DIR
        /
        f"{country}_prices.csv"
    )



    load_file = (
        RAW_LATEST_DIR
        /
        f"{country}_load.csv"
    )



    generation_file = (
        RAW_LATEST_DIR
        /
        f"{country}_generation.csv"
    )



    if not price_file.exists():

        print(
            "No latest prices"
        )

        return



    print(
        "Reading latest data..."
    )



    price = pd.read_csv(
        price_file
    )



    price = price.rename(
        columns={
            "Unnamed: 0":
            "timestamp"
        }
    )


    price["timestamp"] = pd.to_datetime(
        price["timestamp"],
        utc=True
    )


    price = price.rename(
        columns={
            "price_eur_mwh":
            "day_ahead_price"
        }
    )


    price = price[
        [
            "timestamp",
            "day_ahead_price"
        ]
    ]



    # ------------------------------------------------------
    # Merge
    # ------------------------------------------------------

    updated = pd.concat(
        [
            historical,
            price
        ],
        ignore_index=True
    )



    updated = (
        updated
        .drop_duplicates(
            subset=[
                "timestamp"
            ],
            keep="last"
        )
        .sort_values(
            "timestamp"
        )
    )



    # ------------------------------------------------------
    # Save
    # ------------------------------------------------------

    updated.to_csv(
        clean_file,
        index=False
    )



    print(
        "Updated dataset:",
        updated.shape
    )


    print(
        "New max timestamp:",
        updated["timestamp"].max()
    )



# ==========================================================
# MAIN
# ==========================================================


if __name__ == "__main__":


    for country in COUNTRIES:

        try:

            update_country(
                country
            )


        except Exception as e:

            print(
                country,
                "FAILED"
            )

            print(
                e
            )



    print("\n")
    print("="*70)
    print(
        "LIVE DATA UPDATE COMPLETED"
    )
    print("="*70)