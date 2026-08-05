# ==========================================================
# MARKET DATA CLEANING PIPELINE
# Energy Trading Decision Support System
# ==========================================================


import pandas as pd
from pathlib import Path
import sys



# ==========================================================
# PROJECT PATH
# ==========================================================


BASE_DIR = Path(__file__).resolve().parents[2]


sys.path.append(
    str(BASE_DIR)
)



# ==========================================================
# DIRECTORIES
# ==========================================================


RAW_DIR = (

    BASE_DIR
    /
    "data"
    /
    "raw"
    /
    "latest"

)



PROCESSED_DIR = (

    BASE_DIR
    /
    "data"
    /
    "processed"

)



PROCESSED_DIR.mkdir(
    parents=True,
    exist_ok=True
)




# ==========================================================
# CLEAN FUNCTION
# ==========================================================


def clean_dataframe(df):


    # ------------------------------
    # Timestamp handling
    # ------------------------------


    df.index = pd.to_datetime(
        df.index,
        utc=True,
        errors="coerce"
    )


    df = df[
        ~df.index.isna()
    ]



    # sort timestamps

    df = df.sort_index()



    # ------------------------------
    # Remove duplicated columns
    # ------------------------------


    df = df.loc[
        :,
        ~df.columns.duplicated()
    ]



    # ------------------------------
    # Remove empty columns
    # ------------------------------


    df = df.dropna(
        axis=1,
        how="all"
    )



    # ------------------------------
    # Numeric conversion
    # ------------------------------


    for col in df.columns:

        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )



    # ------------------------------
    # Fill missing values
    # ------------------------------


    df = df.ffill()


    df = df.bfill()



    return df




# ==========================================================
# FILE PROCESSOR
# ==========================================================


def process_file(
        input_file,
        output_file
):


    print("\n")
    print("-"*60)

    print(
        "Processing:",
        input_file.name
    )


    df = pd.read_csv(

        input_file,

        index_col=0

    )



    print(
        "Original shape:",
        df.shape
    )



    df = clean_dataframe(
        df
    )



    print(
        "Clean shape:",
        df.shape
    )



    print(
        "Columns:",
        list(df.columns)
    )



    print(
        "Missing:",
        df.isna().sum().sum()
    )



    df.to_csv(
        output_file
    )



    print(
        "Saved:",
        output_file
    )




# ==========================================================
# MAIN
# ==========================================================


def main():


    print("="*70)

    print(
        "ENERGY MARKET DATA CLEANING"
    )

    print("="*70)



    files = list(
        RAW_DIR.glob(
            "*.csv"
        )
    )



    if not files:

        print(
            "No raw files found"
        )

        return




    for file in files:



        output = (

            PROCESSED_DIR

            /

            file.name.replace(
                ".csv",
                "_clean.csv"
            )

        )



        process_file(
            file,
            output
        )




    print("\n")

    print("="*70)

    print(
        "CLEANING COMPLETED"
    )

    print("="*70)





if __name__ == "__main__":

    main()