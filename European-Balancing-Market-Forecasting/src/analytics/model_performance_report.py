from pathlib import Path
import pandas as pd


# =====================================================
# PATHS
# =====================================================

ROOT = Path(__file__).resolve().parents[2]


MODELS_DIR = (
    ROOT
    /
    "models"
)


OUTPUT_DIR = (
    ROOT
    /
    "data"
    /
    "analytics"
)


OUTPUT_DIR.mkdir(
    exist_ok=True
)


COUNTRIES = [
    "germany",
    "france",
    "italy",
    "netherlands",
    "spain"
]


# =====================================================
# COLLECT METRICS
# =====================================================

def collect_metrics(folder):

    results = []


    base = (
        MODELS_DIR
        /
        folder
    )


    for country in COUNTRIES:


        metrics_file = (

            base
            /
            country
            /
            "metrics.csv"

        )


        if metrics_file.exists():


            df = pd.read_csv(
                metrics_file
            )


            df["country"] = country


            results.append(
                df
            )


        else:

            print(
                "Missing:",
                metrics_file
            )


    if len(results)==0:

        return None


    final = pd.concat(
        results,
        ignore_index=True
    )


    return final




# =====================================================
# LOAD FORECASTING
# =====================================================

print("="*70)
print("LOAD MODEL PERFORMANCE")
print("="*70)


load_metrics = collect_metrics(
    "load_forecasting"
)


if load_metrics is not None:


    print(load_metrics)


    load_metrics.to_csv(

        OUTPUT_DIR
        /
        "load_model_performance.csv",

        index=False

    )



# =====================================================
# IMBALANCE FORECASTING
# =====================================================


print()

print("="*70)
print("IMBALANCE MODEL PERFORMANCE")
print("="*70)



imbalance_metrics = collect_metrics(
    "imbalance_forecasting"
)



if imbalance_metrics is not None:


    print(imbalance_metrics)


    imbalance_metrics.to_csv(

        OUTPUT_DIR
        /
        "imbalance_model_performance.csv",

        index=False

    )


print()

print(
    "MODEL PERFORMANCE REPORT COMPLETED"
)