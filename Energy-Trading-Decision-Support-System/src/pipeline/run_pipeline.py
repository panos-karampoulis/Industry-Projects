import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Callable, Optional

# ==========================================================
# PROJECT PATH
# ==========================================================

BASE_DIR = Path(__file__).resolve().parents[2]

sys.path.append(
    str(BASE_DIR)
)


PYTHON = sys.executable



# ==========================================================
# PIPELINE STEPS
# ==========================================================

STEPS = [

    (
        "1. Updating Market Data",
        [
            PYTHON,
            "src/pipeline/update_market_data.py"
        ]
    ),


    (
        "2. Updating Historical Dataset With Live Data",
        [
            PYTHON,
            "src/preprocessing/update_live_dataset.py"
        ]
    ),


    (
        "3. Updating Weather Data",
        [
            PYTHON,
            "src/data/download_weather.py"
        ]
    ),


    (
        "4. Building Features",
        [
            PYTHON,
            "src/features/feature_engineering_v2.py"
        ]
    ),


    (
        "5. Running Load Forecast Models",
        [
            PYTHON,
            "src/forecasting/run_all_load_forecasting.py"
        ]
    ),


    (
        "6. Calculating Imbalance Risk",
        [
            PYTHON,
            "src/risk/run_all_imbalance_risk.py"
        ]
    ),


    (
        "7. Generating Trading Decisions",
        [
            PYTHON,
            "src/decision/trading_decision_engine.py"
        ]
    )

]
# ==========================================================
# RUNNER
# ==========================================================


def run_step(name, command):

    print("\n")
    print("="*80)
    print(name)
    print("="*80)


    result = subprocess.run(
        command,
        cwd=BASE_DIR
    )


    if result.returncode != 0:

        raise RuntimeError(
            f"{name} FAILED"
        )


    print(
        f"✓ {name} COMPLETED"
    )



# ==========================================================
# MAIN PIPELINE
# ==========================================================


def run_pipeline():


    start = datetime.now()


    print("\n")
    print("="*80)
    print(
        "ENERGY TRADING DECISION SUPPORT SYSTEM PIPELINE"
    )
    print("="*80)



    for name, command in STEPS:

        run_step(
            name,
            command
        )



    end = datetime.now()



    print("\n")
    print("="*80)
    print("PIPELINE FINISHED SUCCESSFULLY")
    print("="*80)


    print(
        "Started:",
        start
    )

    print(
        "Finished:",
        end
    )

    print(
        "Duration:",
        end-start
    )


    # save refresh timestamp

    refresh_file = (
        BASE_DIR /
        "data" /
        "last_refresh.txt"
    )


    with open(
        refresh_file,
        "w"
    ) as f:

        f.write(
            str(end)
        )


    print(
        "Refresh timestamp saved:",
        refresh_file
    )



if __name__ == "__main__":

    run_pipeline()