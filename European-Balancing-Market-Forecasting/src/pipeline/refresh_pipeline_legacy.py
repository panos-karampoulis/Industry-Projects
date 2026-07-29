import subprocess
import sys
from pathlib import Path
from datetime import datetime


ROOT = Path(
    r"D:\Portfolio\European-Balancing-Market-Forecasting"
)


PYTHON = sys.executable



SCRIPTS = [

    (
        "Downloading generation data",
        ROOT /
        "src" /
        "data_loader" /
        "generation_downloader.py"
    ),


    (
        "Downloading market data",
        ROOT /
        "src" /
        "data_loader" /
        "market_downloader.py"
    ),


    (
        "Calculating imbalance",
        ROOT /
        "src" /
        "balancing" /
        "imbalance_calculation.py"
    ),


    (
        "Generation feature engineering",
        ROOT /
        "src" /
        "features" /
        "generation_feature_engineering.py"
    ),


    (
        "Market feature engineering",
        ROOT /
        "src" /
        "features" /
        "feature_engineering.py"
    ),


    (
        "Risk feature engineering",
        ROOT /
        "src" /
        "features" /
        "market_risk_features.py"
    ),


    (
        "Generate ML forecast",
        ROOT /
        "src" /
        "forecasting" /
        "ml_next_day_forecast.py"
    )

]



def run_step(
    name,
    script
):

    print("\n")
    print("="*70)
    print(name)
    print("="*70)


    if not script.exists():

        print(
            "Missing script:",
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

        print(
            "FAILED:",
            name
        )

        return False



    print(
        "COMPLETED:",
        name
    )


    return True




def refresh():


    start = datetime.now()


    print(
        """
============================================================
STARTING PLATFORM REFRESH
============================================================
"""
    )


    for name, script in SCRIPTS:


        success = run_step(
            name,
            script
        )


        if not success:

            print(
                "PIPELINE STOPPED"
            )

            return



    end = datetime.now()



    print(
        """
============================================================
REFRESH COMPLETED
============================================================
"""
    )


    print(
        "Duration:",
        end-start
    )




if __name__ == "__main__":

    refresh()