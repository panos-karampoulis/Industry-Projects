import pandas as pd
from pathlib import Path
import sys


# ============================================================
# PATH SETUP
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

sys.path.append(
    str(BASE_DIR)
)



# ============================================================
# IMPORTS
# ============================================================

from src.models.baseline_models import (
    naive_forecast,
    moving_average_forecast,
    simple_exponential_smoothing_forecast,
    holt_winters_forecast,
    arima_forecast,
   
)


from src.models.metrics import (
    calculate_metrics
)


from src.models.plots import (
    plot_forecast
)



# ============================================================
# PATHS
# ============================================================


INPUT_FILE = (
    BASE_DIR
    /
    "data"
    /
    "processed"
    /
    "europe_intraday_weather_features.csv"
)



RESULTS_DIR = (
    BASE_DIR
    /
    "data"
    /
    "results"
)



PLOTS_DIR = (
    RESULTS_DIR
    /
    "plots"
)



METRICS_FILE = (
    RESULTS_DIR
    /
    "baseline_metrics.csv"
)



RESULTS_DIR.mkdir(
    exist_ok=True,
    parents=True
)



# ============================================================
# LOAD DATA
# ============================================================


print("="*60)
print("Loading dataset")
print("="*60)


df = pd.read_csv(
    INPUT_FILE,
    parse_dates=[
        "timestamp"
    ]
)



print(
    df.shape
)



# ============================================================
# CLEAN
# ============================================================


df = (

    df
    .sort_values(
        [
            "country",
            "timestamp"
        ]
    )

)



df = (

    df
    .drop_duplicates(
        subset=[
            "country",
            "timestamp"
        ]
    )

)



# ============================================================
# MODELS
# ============================================================


models = {

    "Naive":
        naive_forecast,


    "Moving_Average":
        moving_average_forecast,


    "Exponential_Smoothing":
        simple_exponential_smoothing_forecast,


    "Holt_Winters":
        holt_winters_forecast,


    "ARIMA":
        arima_forecast,


 
}



# ============================================================
# TRAIN LOOP
# ============================================================


all_results = []



countries = (

    df["country"]
    .unique()

)



for country in countries:


    print()
    print("="*60)
    print(country.upper())
    print("="*60)



    country_df = (

        df[
            df["country"]
            ==
            country
        ]

        .copy()

    )



    country_df = (

        country_df
        .sort_values(
            "timestamp"
        )

    )



    series = (

        country_df
        .set_index(
            "timestamp"
        )
        [
            "price_eur_mwh"
        ]

    )



    # remove duplicates

    series = (

        series[
            ~series.index.duplicated(
                keep="first"
            )
        ]

    )



    # 80/20 split

    split = int(
        len(series)
        *
        0.8
    )


    train = series.iloc[:split]

    test = series.iloc[split:]



    print(
        "Train:",
        len(train),
        "Test:",
        len(test)
    )



    for model_name, model_func in models.items():


        print(
            "Running",
            model_name
        )


        try:


            prediction = model_func(
                train,
                test
            )



            metrics = calculate_metrics(
                test,
                prediction
            )



            result = {


                "country":
                    country,


                "model":
                    model_name,


                **metrics

            }


            all_results.append(
                result
            )



            plot_forecast(

                test,

                prediction,

                country,

                model_name,

                PLOTS_DIR

            )



        except Exception as e:


            print(
                "FAILED:",
                model_name,
                e
            )



# ============================================================
# SAVE RESULTS
# ============================================================


results_df = pd.DataFrame(
    all_results
)



results_df = results_df.sort_values(
    [
        "country",
        "RMSE"
    ]
)



results_df.to_csv(
    METRICS_FILE,
    index=False
)



print()
print("="*60)
print("BASELINE TRAINING COMPLETED")
print("="*60)


print(
    results_df
)



print()

print(
    "Saved:",
    METRICS_FILE
)