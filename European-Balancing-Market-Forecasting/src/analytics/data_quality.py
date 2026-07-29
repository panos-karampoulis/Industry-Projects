import pandas as pd
from pathlib import Path


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

RAW_DIR = (
    BASE_DIR
    /
    "data"
    /
    "raw"
)


# ============================================================
# QUALITY CHECKS
# ============================================================


def check_dataset(
        file_path,
        country,
        dataset_name
):

    print("\n")
    print("=" * 70)
    print(f"{country.upper()} - {dataset_name.upper()}")
    print("=" * 70)


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


    start = df["timestamp"].min()

    end = df["timestamp"].max()


    duplicates = (
        df["timestamp"]
        .duplicated()
        .sum()
    )


    freq_series = (
        df["timestamp"]
        .diff()
        .dropna()
    )


    frequency = (
        freq_series
        .mode()[0]
        if not freq_series.empty
        else None
    )


    missing_values = (
        df.isna()
        .sum()
        .sum()
    )


    print(
        f"Rows: {len(df)}"
    )


    print(
        f"Start: {start}"
    )


    print(
        f"End: {end}"
    )


    print(
        f"Frequency: {frequency}"
    )


    print(
        f"Duplicate timestamps: {duplicates}"
    )


    print(
        f"Missing values: {missing_values}"
    )


    if "load_mw" in df.columns:

        print("\nLOAD STATISTICS")

        print(
            df["load_mw"]
            .describe()
        )


    if "price_eur_mwh" in df.columns:

        print("\nPRICE STATISTICS")

        print(
            df["price_eur_mwh"]
            .describe()
        )


        negative_prices = (
            df["price_eur_mwh"]
            <
            0
        ).sum()


        print(
            f"Negative prices: {negative_prices}"
        )


    return {

        "country": country,

        "dataset": dataset_name,

        "rows": len(df),

        "start": start,

        "end": end,

        "frequency": str(frequency),

        "duplicates": duplicates,

        "missing_values": missing_values

    }



# ============================================================
# RUN ALL COUNTRIES
# ============================================================


def run_quality_report():


    results = []


    countries = [

        x.name

        for x in RAW_DIR.iterdir()

        if x.is_dir()

    ]


    for country in countries:


        country_dir = (
            RAW_DIR
            /
            country
        )


        files = {


            "load":
            country_dir
            /
            "load.csv",


            "prices":
            country_dir
            /
            "day_ahead_prices.csv"

        }



        for name, file in files.items():


            if file.exists():


                result = check_dataset(

                    file,

                    country,

                    name

                )


                results.append(
                    result
                )


    report = pd.DataFrame(
        results
    )


    output = (
        BASE_DIR
        /
        "data"
        /
        "quality_report.csv"
    )


    report.to_csv(
        output,
        index=False
    )


    print("\n")
    print("="*70)
    print("QUALITY REPORT SAVED")
    print(output)
    print("="*70)



if __name__ == "__main__":

    run_quality_report()