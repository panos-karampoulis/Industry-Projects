import subprocess
import sys
from pathlib import Path
from datetime import datetime

sys.stdout.reconfigure(
    encoding="utf-8"
)
# ============================================================
# PROJECT ROOT
# ============================================================

ROOT = Path(__file__).resolve().parents[2]

PYTHON = sys.executable



# ============================================================
# PIPELINE STEPS
# ============================================================

SCRIPTS = [

    (
        "Generation incremental refresh",

        ROOT
        /
        "src"
        /
        "data_loader"
        /
        "generation_incremental_update.py"
    ),


    (
        "Load incremental refresh",

        ROOT
        /
        "src"
        /
        "data_loader"
        /
        "load_incremental_update.py"
    ),


    (
        "Price incremental refresh",

        ROOT
        /
        "src"
        /
        "data_loader"
        /
        "price_incremental_update.py"
    ),


    (
        "Calculate imbalance",

        ROOT
        /
        "src"
        /
        "balancing"
        /
        "imbalance_calculation.py"
    ),


    (
        "Generation feature engineering",

        ROOT
        /
        "src"
        /
        "features"
        /
        "generation_feature_engineering.py"
    ),


    (
        "Market feature engineering",

        ROOT
        /
        "src"
        /
        "features"
        /
        "feature_engineering.py"
    ),


    (
        "Risk feature engineering",

        ROOT
        /
        "src"
        /
        "features"
        /
        "market_risk_features.py"
    ),


    (
        "ML next day forecasting",

        ROOT
        /
        "src"
        /
        "forecasting"
        /
        "ml_next_day_forecast.py"
    )

]



# ============================================================
# RUN SINGLE STEP
# ============================================================

def run_step(name, script):


    print("\n")
    print("=" * 80)
    print(name)
    print("=" * 80)



    if not script.exists():

        print(
            "MISSING SCRIPT:"
        )

        print(
            script
        )

        return False



    result = subprocess.run(

        [
            PYTHON,
            str(script)

        ],

        cwd=ROOT

    )



    if result.returncode != 0:


        print()

        print(
            "FAILED:",
            name
        )


        return False



    print()

    print(
        "COMPLETED:",
        name
    )


    return True




# ============================================================
# FULL PLATFORM REFRESH
# ============================================================

def refresh():


    start = datetime.now()


    print(
"""
============================================================
EUROPEAN BALANCING MARKET PLATFORM REFRESH
============================================================

Starting incremental data refresh...

Project:
{root}

Python:
{python}

""".format(

    root=ROOT,

    python=PYTHON

)

    )



    completed = []



    for name, script in SCRIPTS:



        success = run_step(

            name,

            script

        )



        if not success:


            print()

            print(
"""
============================================================
PIPELINE STOPPED
============================================================
"""
            )


            print(
                "Failed step:",
                name
            )


            return False



        completed.append(
            name
        )



    duration = datetime.now() - start



    print()

    print("=" * 80)

    print(
        "REFRESH COMPLETED SUCCESSFULLY"
    )

    print("=" * 80)



    print()

    print(
        "Duration:",
        duration
    )



    print()

    print(
        "Completed steps:"
    )



    for step in completed:

        print(
            "[OK]",
            step
        )



    return True




# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":


    refresh()