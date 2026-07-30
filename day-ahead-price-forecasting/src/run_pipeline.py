import os
import subprocess
import argparse
from pathlib import Path


# ============================================================
# Project paths
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]


FEATURE_SCRIPT = (
    BASE_DIR
    / "src"
    / "features"
    / "feature_engineering.py"
)


MERGE_SCRIPT = (
    BASE_DIR
    / "src"
    / "features"
    / "merge_market_weather.py"
)


COMBINE_SCRIPT = (
    BASE_DIR
    / "src"
    / "features"
    / "combine_year_dataset.py"
)



# ============================================================
# Run command
# ============================================================

def run_command(command):

    print("\n")
    print("=" * 70)
    print("Running:")
    

    # IMPORTANT:
    # Use the same python interpreter
    # that runs this pipeline
    command[0] = os.sys.executable


    print(" ".join(command))

    print("=" * 70)


    result = subprocess.run(
        command,
        cwd=BASE_DIR
    )


    if result.returncode != 0:
        raise RuntimeError(
            f"\nFailed command:\n{command}"
        )



# ============================================================
# Monthly pipeline
# ============================================================

def run_month_pipeline(
        country,
        year,
        month
):

    month = str(month).zfill(2)


    print("\n")
    print("#" * 70)
    print(
        f"PROCESSING {country.upper()} "
        f"{year}-{month}"
    )
    print("#" * 70)



    # --------------------------------------------------------
    # 1. Feature Engineering
    # --------------------------------------------------------

    run_command(
        [
            "python",
            str(FEATURE_SCRIPT),
            "--country",
            country,
            "--year",
            str(year),
            "--month",
            month
        ]
    )



    # --------------------------------------------------------
    # 2. Merge Market + Weather
    # --------------------------------------------------------

    run_command(
        [
            "python",
            str(MERGE_SCRIPT),
            "--country",
            country,
            "--year",
            str(year),
            "--month",
            month
        ]
    )




# ============================================================
# Year pipeline
# ============================================================

def run_year_pipeline(
        country,
        year
):


    for month in range(1,13):

        run_month_pipeline(
            country,
            year,
            month
        )



    # --------------------------------------------------------
    # 3. Combine yearly dataset
    # --------------------------------------------------------

    run_command(
        [
            "python",
            str(COMBINE_SCRIPT),
            "--country",
            country,
            "--year",
            str(year)
        ]
    )




# ============================================================
# Main
# ============================================================

def main():

    parser = argparse.ArgumentParser(
        description="Day Ahead Price Forecasting Pipeline"
    )


    parser.add_argument(
        "--country",
        default="germany"
    )


    parser.add_argument(
        "--start_year",
        type=int,
        default=2020
    )


    parser.add_argument(
        "--end_year",
        type=int,
        default=2026
    )


    args = parser.parse_args()



    print("=" * 70)
    print(
        "DAY AHEAD PRICE FORECASTING PIPELINE"
    )
    print("=" * 70)


    print(
        f"Country: {args.country}"
    )

    print(
        f"Years: {args.start_year}-{args.end_year}"
    )



    for year in range(
        args.start_year,
        args.end_year + 1
    ):


        run_year_pipeline(
            args.country,
            year
        )



    print("\n")
    print("=" * 70)
    print(
        "PIPELINE COMPLETED SUCCESSFULLY"
    )
    print("=" * 70)




if __name__ == "__main__":

    main()