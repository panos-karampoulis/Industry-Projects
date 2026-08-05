import pandas as pd
from pathlib import Path


# ==========================================================
# PROJECT PATH
# ==========================================================

BASE_DIR = Path(__file__).resolve().parents[2]


DATA_DIR = (
    BASE_DIR
    /
    "data"
    /
    "raw"
    /
    "latest"
)


# ==========================================================
# COUNTRIES
# ==========================================================

COUNTRIES = [

    "germany",
    "netherlands",
    "france",
    "spain",
    "italy"

]


# ==========================================================
# FILE CHECKER
# ==========================================================


def check_file(
    file_path,
    data_type
):


    print("\n")
    print("-" * 60)
    print(data_type.upper())
    print("-" * 60)


    if not file_path.exists():

        print(
            "STATUS: FILE NOT FOUND"
        )

        return



    try:

        df = pd.read_csv(
            file_path,
            index_col=0
        )


        # datetime index

        df.index = pd.to_datetime(
            df.index,
            utc=True,
            errors="coerce"
        )


        # remove invalid dates

        df = df[
            df.index.notna()
        ]


        print(
            "Rows:",
            len(df)
        )


        print(
            "Columns:",
            list(df.columns)
        )


        print(
            "Missing values:",
            int(df.isna().sum().sum())
        )


        print(
            "Duplicate timestamps:",
            int(df.index.duplicated().sum())
        )


        if len(df) > 1:


            diff = (
                df.index
                .to_series()
                .diff()
                .dropna()
            )


            frequency = (
                diff.mode()[0]
            )


            print(
                "Frequency:",
                frequency
            )


        print(
            "Start:",
            df.index.min()
        )


        print(
            "End:",
            df.index.max()
        )



        # ==================================================
        # PRICE SPECIFIC CHECKS
        # ==================================================

        if data_type == "prices":


            price_col = df.columns[0]


            negative = (
                df[price_col] < 0
            ).sum()


            print(
                "Negative prices:",
                int(negative)
            )


            print(
                "Average price:",
                round(
                    df[price_col].mean(),
                    2
                )
            )


            print(
                "Maximum price:",
                round(
                    df[price_col].max(),
                    2
                )
            )


            print(
                "Minimum price:",
                round(
                    df[price_col].min(),
                    2
                )
            )



        print(
            "STATUS: OK"
        )


    except Exception as e:


        print(
            "STATUS: FAILED"
        )


        print(
            e
        )



# ==========================================================
# COUNTRY REPORT
# ==========================================================


def check_country(
    country
):


    print("\n")
    print("=" * 60)
    print(
        country.upper()
    )
    print("=" * 60)



    files = {


        "load":
        DATA_DIR
        /
        f"{country}_load.csv",


        "prices":
        DATA_DIR
        /
        f"{country}_prices.csv",


        "generation":
        DATA_DIR
        /
        f"{country}_generation.csv"


    }



    for data_type, path in files.items():


        check_file(
            path,
            data_type
        )



# ==========================================================
# MAIN
# ==========================================================


def main():


    print("=" * 70)

    print(
        "ENERGY MARKET DATA QUALITY REPORT"
    )

    print("=" * 70)



    for country in COUNTRIES:


        check_country(
            country
        )



    print("\n")
    print("=" * 70)

    print(
        "QUALITY CHECK COMPLETED"
    )

    print("=" * 70)



if __name__ == "__main__":

    main()