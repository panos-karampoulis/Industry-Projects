import os
import time
import joblib
import warnings

import numpy as np
import pandas as pd

from pathlib import Path


from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)


from xgboost import XGBRegressor


warnings.filterwarnings("ignore")


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]


DATA_FILE = (
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


MODELS_DIR = (
    BASE_DIR
    /
    "models"
)



RESULTS_DIR.mkdir(
    exist_ok=True,
    parents=True
)


MODELS_DIR.mkdir(
    exist_ok=True,
    parents=True
)



# ============================================================
# CONFIGURATION
# ============================================================


COUNTRIES = [

    "france",
    "germany",
    "italy",
    "netherlands",
    "spain"

]



TARGET = "price_eur_mwh"



FEATURES = [

    # Time features

    "hour",
    "day_of_week",
    "month",
    "weekend",
    "dst_flag",

    "is_peak",
    "is_off_peak",
    "night_period",
    "morning_ramp",
    "evening_peak",


    # Lag features

    "lag_1",
    "lag_4",
    "lag_96",
    "lag_672",


    # Rolling statistics

    "rolling_mean_96",
    "rolling_std_96",
    "rolling_mean_672",


    # Weather

    "temperature_2m",
    "wind_speed_10m",
    "shortwave_radiation",
    "cloud_cover",
    "precipitation"

]



# ============================================================
# METRICS
# ============================================================


def smape(
    y_true,
    y_pred
):

    denominator = (
        np.abs(y_true)
        +
        np.abs(y_pred)
        +
        1e-8
    )


    return (
        100
        *
        np.mean(
            2
            *
            np.abs(
                y_pred - y_true
            )
            /
            denominator
        )
    )



def evaluate_model(
    y_true,
    y_pred
):


    return {

        "MAE":
            round(
                mean_absolute_error(
                    y_true,
                    y_pred
                ),
                4
            ),


        "RMSE":
            round(
                np.sqrt(
                    mean_squared_error(
                        y_true,
                        y_pred
                    )
                ),
                4
            ),


        "R2":
            round(
                r2_score(
                    y_true,
                    y_pred
                ),
                4
            ),


        "sMAPE":
            round(
                smape(
                    y_true,
                    y_pred
                ),
                4
            )

    }



# ============================================================
# MODELS
# ============================================================


def get_models():


    models = {


        "Linear_Regression":

            LinearRegression(),



        "Random_Forest":

            RandomForestRegressor(

                n_estimators=300,

                max_depth=12,

                random_state=42,

                n_jobs=-1

            ),



        "XGBoost":

            XGBRegressor(

                n_estimators=500,

                learning_rate=0.05,

                max_depth=8,

                subsample=0.8,

                colsample_bytree=0.8,

                random_state=42,

                n_jobs=-1,

                objective="reg:squarederror"

            )

    }


    return models



# ============================================================
# LOAD DATA
# ============================================================


print("="*60)

print(
    "Loading dataset"
)

print("="*60)



df = pd.read_csv(
    DATA_FILE,
    parse_dates=[
        "timestamp"
    ]
)



print(
    df.shape
)



print(
    df.head()
)

# ============================================================
# TRAINING LOOP
# ============================================================


all_results = []



all_feature_importance = []



print("\n")



for country in COUNTRIES:


    print("="*60)

    print(
        country.upper()
    )

    print("="*60)



    country_df = (

        df[
            df["country"] == country
        ]

        .copy()

        .sort_values(
            "timestamp"
        )

    )



    print(
        "Rows:",
        len(country_df)
    )



    # --------------------------------------------------------
    # FEATURES / TARGET
    # --------------------------------------------------------


    X = (

        country_df[FEATURES]

        .copy()

    )


    y = (

        country_df[TARGET]

        .copy()

    )



    # remove missing values

    data = pd.concat(
        [
            X,
            y
        ],
        axis=1
    )


    data = data.dropna()



    X = data[FEATURES]

    y = data[TARGET]



    # --------------------------------------------------------
    # TIME SPLIT
    # --------------------------------------------------------


    split_index = int(
        len(data)
        *
        0.8
    )



    X_train = (

        X.iloc[
            :split_index
        ]

    )


    X_test = (

        X.iloc[
            split_index:
        ]

    )


    y_train = (

        y.iloc[
            :split_index
        ]

    )


    y_test = (

        y.iloc[
            split_index:
        ]

    )



    print(
        "Train:",
        len(X_train),
        "Test:",
        len(X_test)
    )



    # --------------------------------------------------------
    # MODELS
    # --------------------------------------------------------


    models = get_models()



    for model_name, model in models.items():


        print(
            "Running",
            model_name
        )



        start_time = time.time()



        try:


            # Train

            model.fit(
                X_train,
                y_train
            )



            # Prediction

            predictions = (

                model.predict(
                    X_test
                )

            )



            training_time = (

                time.time()
                -
                start_time

            )



            metrics = evaluate_model(

                y_test,

                predictions

            )



            result = {


                "country":
                    country,


                "model":
                    model_name,


                "training_time_sec":
                    round(
                        training_time,
                        2
                    ),


                **metrics

            }



            all_results.append(
                result
            )



            # ------------------------------------------------
            # SAVE MODEL
            # ------------------------------------------------


            country_model_dir = (

                MODELS_DIR

                /

                country

            )


            country_model_dir.mkdir(

                exist_ok=True,

                parents=True

            )



            model_path = (

                country_model_dir

                /

                f"{model_name}.joblib"

            )



            joblib.dump(

                model,

                model_path

            )



            # ------------------------------------------------
            # SAVE PREDICTIONS
            # ------------------------------------------------


            predictions_df = pd.DataFrame(

                {


                    "timestamp":
                    country_df[
                        "timestamp"
                    ]
                    .iloc[
                        split_index:
                    ]
                    .values,


                    "actual":
                    y_test.values,


                    "prediction":
                    predictions


                }

            )



            prediction_file = (

                RESULTS_DIR

                /

                f"{country}_{model_name}_predictions.csv"

            )



            predictions_df.to_csv(

                prediction_file,

                index=False

            )



            # ------------------------------------------------
            # FEATURE IMPORTANCE
            # ------------------------------------------------


            if hasattr(

                model,

                "feature_importances_"

            ):


                importance = pd.DataFrame(

                    {


                        "feature":
                        FEATURES,


                        "importance":
                        model.feature_importances_,


                        "country":
                        country,


                        "model":
                        model_name


                    }

                )


                all_feature_importance.append(

                    importance

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



results_file = (

    RESULTS_DIR

    /

    "ml_metrics.csv"

)



results_df.to_csv(

    results_file,

    index=False

)



print("\n")

print("="*60)

print(
    "ML TRAINING COMPLETED"
)

print("="*60)



print(
    results_df
    .sort_values(
        [
            "country",
            "RMSE"
        ]
    )
)



print()

print(
    "Saved:",
    results_file
)



# ============================================================
# SAVE FEATURE IMPORTANCE
# ============================================================


if len(all_feature_importance) > 0:


    feature_df = pd.concat(

        all_feature_importance,

        ignore_index=True

    )


    feature_file = (

        RESULTS_DIR

        /

        "feature_importance.csv"

    )


    feature_df.to_csv(

        feature_file,

        index=False

    )


    print(

        "Saved:",

        feature_file

    )

# ============================================================
# MODEL RANKING
# ============================================================


print("\n")

print("="*60)

print(
    "MODEL RANKING"
)

print("="*60)



ranking_df = (

    results_df

    .sort_values(
        [
            "country",
            "RMSE"
        ]
    )

)



best_models = (

    ranking_df

    .groupby(
        "country"
    )

    .first()

    .reset_index()

)



best_file = (

    RESULTS_DIR

    /

    "best_models_by_country.csv"

)



best_models.to_csv(

    best_file,

    index=False

)



print(best_models)



print()

print(
    "Saved:",
    best_file
)




# ============================================================
# VISUALIZATION
# ============================================================


import matplotlib.pyplot as plt




PLOT_DIR = (

    BASE_DIR

    /

    "images"

    /

    "ml_results"

)



PLOT_DIR.mkdir(

    exist_ok=True,

    parents=True

)




print()

print("="*60)

print(
    "Creating plots"
)

print("="*60)





for country in COUNTRIES:



    country_results = results_df[

        results_df["country"]

        ==
        country

    ]



    if len(country_results)==0:

        continue



    best_model = (

        country_results

        .sort_values(
            "RMSE"
        )

        .iloc[0]["model"]

    )



    prediction_file = (

        RESULTS_DIR

        /

        f"{country}_{best_model}_predictions.csv"

    )



    if not prediction_file.exists():

        continue



    pred_df = pd.read_csv(

        prediction_file,

        parse_dates=[
            "timestamp"
        ]

    )




    # --------------------------------------------------------
    # Actual vs Prediction
    # --------------------------------------------------------


    plt.figure(
        figsize=(12,5)
    )


    plt.plot(

        pred_df["timestamp"]
        .iloc[:500],

        pred_df["actual"]
        .iloc[:500],

        label="Actual"

    )


    plt.plot(

        pred_df["timestamp"]
        .iloc[:500],

        pred_df["prediction"]
        .iloc[:500],

        label="Prediction"

    )


    plt.title(

        f"{country.upper()} - {best_model} Forecast"

    )


    plt.xlabel(
        "Time"
    )


    plt.ylabel(
        "Price EUR/MWh"
    )


    plt.legend()


    plt.xticks(
        rotation=45
    )


    plt.tight_layout()



    plt.savefig(

        PLOT_DIR

        /

        f"{country}_prediction.png",

        dpi=300

    )


    plt.close()



    # --------------------------------------------------------
    # Residual plot
    # --------------------------------------------------------


    pred_df["residual"] = (

        pred_df["actual"]

        -

        pred_df["prediction"]

    )



    plt.figure(

        figsize=(10,4)

    )


    plt.plot(

        pred_df["residual"]
        .iloc[:500]

    )


    plt.title(

        f"{country.upper()} Residuals"

    )


    plt.xlabel(
        "Observation"
    )


    plt.ylabel(
        "Error"
    )


    plt.tight_layout()



    plt.savefig(

        PLOT_DIR

        /

        f"{country}_residuals.png",

        dpi=300

    )


    plt.close()



print()

print("="*60)

print(
    "ALL DONE"
)

print("="*60)



print(
    "Plots saved:",
    PLOT_DIR
)