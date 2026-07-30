from pathlib import Path
import sys
import subprocess
import time
from datetime import datetime



# ==================================================
# Paths
# ==================================================

BASE_DIR = Path(__file__).resolve().parents[2]

sys.path.append(
    str(BASE_DIR)
)

sys.path.append(
    str(BASE_DIR / "src")
)


from config.countries import COUNTRIES



# ==================================================
# Configuration
# ==================================================

START_YEAR = 2020

END_YEAR = 2020


COUNTRIES_TO_RUN = [

    "Germany",
    

]


# 2026 available months
CURRENT_YEAR_MONTH = 7



# ==================================================
# Logs
# ==================================================

LOG_DIR = Path(
    "logs"
)

LOG_DIR.mkdir(
    exist_ok=True
)


ERROR_LOG = (
    LOG_DIR
    /
    "pipeline_errors.log"
)



# ==================================================
# Command runner
# ==================================================

def run_command(command):


    print("\n")

    print("="*70)

    print(command)

    print("="*70)



    try:

        subprocess.run(

            command,

            shell=True,

            check=True

        )


        return True



    except subprocess.CalledProcessError as e:


        error_message = (

            f"\n[{datetime.now()}]\n"

            f"FAILED COMMAND:\n"

            f"{command}\n"

            f"{e}\n"

        )


        print(
            error_message
        )


        with open(
            ERROR_LOG,
            "a",
            encoding="utf-8"
        ) as f:

            f.write(
                error_message
            )


        return False



# ==================================================
# Months
# ==================================================

def get_months(year):


    if year == 2026:

        return range(
            1,
            CURRENT_YEAR_MONTH + 1
        )


    return range(
        1,
        13
    )



# ==================================================
# Check completed
# ==================================================

def dataset_exists(
    country,
    year,
    month
):


    file = (

        Path("data/final")

        /

        country.lower()

        /

        str(year)

        /

        f"{month:02d}"

        /

        "day_ahead_dataset.csv"

    )


    return file.exists()



# ==================================================
# Main
# ==================================================

def main():


    print("="*70)

    print(
        "FULL DAY AHEAD PRICE FORECASTING PIPELINE"
    )

    print("="*70)



    total = 0


    for country in COUNTRIES_TO_RUN:

        for year in range(
            START_YEAR,
            END_YEAR + 1
        ):

            total += len(
                list(
                    get_months(year)
                )
            )



    counter = 0



    for country in COUNTRIES_TO_RUN:


        print("\n")

        print("#"*70)

        print(
            f"COUNTRY: {country}"
        )

        print("#"*70)



        for year in range(
            START_YEAR,
            END_YEAR + 1
        ):



            for month in get_months(year):


                counter += 1



                print("\n")

                print("-"*70)

                print(
                    f"[{counter}/{total}]"
                )

                print(
                    f"{country} {year}-{month:02d}"
                )

                print("-"*70)



                # ------------------------------
                # Skip existing
                # ------------------------------

                if dataset_exists(
                    country,
                    year,
                    month
                ):


                    print(
                        "Dataset already exists - skipping"
                    )

                    continue



                # ------------------------------
                # 1 ENTSO-E
                # ------------------------------

                success = run_command(

                    f"python src/data/download_entsoe_data.py "
                    f"--country {country} "
                    f"--year {year} "
                    f"--month {month}"

                )


                if not success:

                    continue



                # ------------------------------
                # 2 Weather
                # ------------------------------

                success = run_command(

                    f"python src/data/download_weather_data.py "
                    f"--country {country} "
                    f"--year {year} "
                    f"--month {month}"

                )


                if not success:

                    continue



                # ------------------------------
                # 3 Hourly
                # ------------------------------

                success = run_command(

                    f"python src/features/create_hourly_dataset.py "
                    f"--country {country} "
                    f"--year {year} "
                    f"--month {month}"

                )


                if not success:

                    continue



                # ------------------------------
                # 4 Features
                # ------------------------------

                success = run_command(

                    f"python src/features/feature_engineering.py "
                    f"--country {country} "
                    f"--year {year} "
                    f"--month {month}"

                )


                if not success:

                    continue



                # ------------------------------
                # 5 Merge
                # ------------------------------

                success = run_command(

                    f"python src/features/merge_market_weather.py "
                    f"--country {country} "
                    f"--year {year} "
                    f"--month {month}"

                )


                if success:


                    print(

                        f"\nCOMPLETED: "
                        f"{country} {year}-{month:02d}"

                    )



                else:


                    print(

                        f"\nFAILED FINAL MERGE: "
                        f"{country} {year}-{month:02d}"

                    )



                # API safety

                time.sleep(2)



    print("\n")

    print("="*70)

    print(
        "FULL PIPELINE COMPLETED"
    )

    print("="*70)



if __name__ == "__main__":

    main()