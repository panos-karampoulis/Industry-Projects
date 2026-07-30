import os
import subprocess
from datetime import datetime


BASE_PATH = r"D:\Portfolio\Intraday Market Forecasting - updated"


PYTHON = os.path.join(
    BASE_PATH,
    "venv",
    "Scripts",
    "python.exe"
)


SCRIPTS = [

    (
        "Updating intraday prices",
        os.path.join(
            BASE_PATH,
            "src",
            "data",
            "update_intraday_prices.py"
        )
    ),


    (
        "Updating day ahead prices",
        os.path.join(
            BASE_PATH,
            "src",
            "data",
            "update_day_ahead_prices.py"
        )
    ),


    (
        "Updating weather data",
        os.path.join(
            BASE_PATH,
            "src",
            "data",
            "download_weather.py"
        )
    ),


    (
        "Building feature dataset",
        os.path.join(
            BASE_PATH,
            "src",
            "processing",
            "build_intraday_weather_features.py"
        )
    ),


    (
        "Generating intraday forecasts",
        os.path.join(
            BASE_PATH,
            "src",
            "forecasting",
            "intraday_forecast_generator.py"
        )
    ),


    (
        "Generating day ahead forecast",
        os.path.join(
            BASE_PATH,
            "src",
            "forecasting",
            "day_ahead_forecast.py"
        )
    ),


    (
        "Generating long term forecast",
        os.path.join(
            BASE_PATH,
            "src",
            "forecasting",
            "day_ahead_long_term_forecast.py"
        )
    )

]



def run_script(name, script):

    print("\n")
    print("="*70)
    print(name)
    print("="*70)


    result = subprocess.run(
        [
            PYTHON,
            script
        ],
        cwd=BASE_PATH,
        capture_output=False
    )


    if result.returncode != 0:

        raise Exception(
            f"Failed: {name}"
        )


    print(
        f"Completed: {name}"
    )




def main():


    start = datetime.now()


    print("="*70)
    print("ENERGY MARKET DATA REFRESH")
    print("="*70)


    for name, script in SCRIPTS:

        run_script(
            name,
            script
        )


    end = datetime.now()


    print("\n")
    print("="*70)
    print("REFRESH COMPLETED")
    print("="*70)


    print(
        "Started:",
        start
    )

    print(
        "Finished:",
        end
    )


    # save timestamp

    timestamp_file = os.path.join(
        BASE_PATH,
        "data",
        "last_refresh.txt"
    )


    with open(
        timestamp_file,
        "w"
    ) as f:

        f.write(
            str(end)
        )


    print(
        "Saved:",
        timestamp_file
    )



if __name__ == "__main__":

    main()