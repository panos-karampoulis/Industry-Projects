import pandas as pd
import numpy as np
import os
import argparse
import pickle
import warnings

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error
)

from lightgbm import LGBMRegressor

warnings.filterwarnings("ignore")


# ============================================================
# ARGUMENTS
# ============================================================

def parse_arguments():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--country",
        type=str,
        required=True
    )

    return parser.parse_args()


# ============================================================
# PATHS
# ============================================================

def get_paths(country):

    feature_file = (
        f"data/features/{country}_features.csv"
    )

    model_path = (
        f"models/{country}/lightgbm_model.pkl"
    )

    result_path = (
        f"results/{country}/lightgbm_results.csv"
    )

    prediction_path = (
        f"results/{country}/lightgbm_predictions.csv"
    )

    os.makedirs(
        f"models/{country}",
        exist_ok=True
    )

    os.makedirs(
        f"results/{country}",
        exist_ok=True
    )

    return (
        feature_file,
        model_path,
        result_path,
        prediction_path
    )


# ============================================================
# LOAD DATA
# ============================================================

def load_dataset(country):

    (
        feature_file,
        _,
        _,
        _
    ) = get_paths(country)

    print("=" * 70)
    print("LIGHTGBM FORECASTING")
    print("=" * 70)

    print()

    print("Country:", country)

    print()

    df = pd.read_csv(
        feature_file,
        index_col=0,
        parse_dates=True
    )

    df = df.sort_index()

    print("Dataset:")

    print(df.shape)

    return df


# ============================================================
# TRAIN TEST SPLIT
# ============================================================

def split_dataset(df):

    target = "price_eur_mwh"

    features = [

        c

        for c in df.columns

        if c != target

    ]

    X = df[features]

    y = df[target]

    split = int(

        len(df) * 0.80

    )

    X_train = X.iloc[:split]

    X_test = X.iloc[split:]

    y_train = y.iloc[:split]

    y_test = y.iloc[split:]

    print()

    print("Train:")

    print(X_train.shape)

    print()

    print("Test:")

    print(X_test.shape)

    return (

        X_train,

        X_test,

        y_train,

        y_test,

        features

    )


# ============================================================
# MODEL
# ============================================================

def train_model(

    X_train,

    y_train

):

    print()

    print("Training LightGBM...")

    model = LGBMRegressor(

        n_estimators=500,

        learning_rate=0.05,

        max_depth=8,

        num_leaves=31,

        subsample=0.8,

        colsample_bytree=0.8,

        random_state=42

    )

    model.fit(

        X_train,

        y_train

    )

    print("Training completed")

    return model


# ============================================================
# PREDICTIONS
# ============================================================

def predict(

    model,

    X_test

):

    print()

    print("Creating predictions...")

    predictions = model.predict(

        X_test

    )

    return predictions

# ============================================================
# METRICS
# ============================================================

def evaluate_model(

    y_test,

    predictions

):

    mae = mean_absolute_error(

        y_test,

        predictions

    )


    rmse = np.sqrt(

        mean_squared_error(

            y_test,

            predictions

        )

    )


    print()

    print("RESULTS")

    print(

        f"MAE: {mae:.4f}"

    )

    print(

        f"RMSE: {rmse:.4f}"

    )


    return mae, rmse



# ============================================================
# FEATURE IMPORTANCE
# ============================================================

def show_feature_importance(

    model,

    features

):

    importance = pd.DataFrame({

        "feature":

            features,


        "importance":

            model.feature_importances_

    })


    importance = importance.sort_values(

        by="importance",

        ascending=False

    )


    print()

    print("TOP FEATURES")

    print(

        importance.head(10)

    )


    return importance



# ============================================================
# SAVE MODEL
# ============================================================

def save_model(

    model,

    path

):

    with open(

        path,

        "wb"

    ) as f:


        pickle.dump(

            model,

            f

        )


    print()

    print("Saved model:")

    print(path)



# ============================================================
# SAVE RESULTS
# ============================================================

def save_results(

    country,

    mae,

    rmse,

    predictions,

    y_test,

    model,

    features

):

    (

        _,

        model_path,

        result_path,

        prediction_path

    ) = get_paths(country)



    # -------------------------
    # metrics
    # -------------------------

    results = pd.DataFrame({

        "model":[

            "LightGBM"

        ],

        "MAE":[

            mae

        ],

        "RMSE":[

            rmse

        ]

    })


    results.to_csv(

        result_path,

        index=False

    )



    # -------------------------
    # predictions
    # -------------------------

    prediction_df = pd.DataFrame({

        "actual":

            y_test,


        "lightgbm_prediction":

            predictions

    })


    prediction_df.to_csv(

        prediction_path

    )



    # -------------------------
    # feature importance
    # -------------------------

    importance = show_feature_importance(

        model,

        features

    )


    importance.to_csv(

        f"results/{country}/lightgbm_feature_importance.csv",

        index=False

    )



    # -------------------------
    # model

    # -------------------------

    save_model(

        model,

        model_path

    )



    print()

    print("Saved:")

    print(result_path)

    print(prediction_path)



# ============================================================
# MAIN PIPELINE
# ============================================================

def main():


    args = parse_arguments()


    country = (

        args.country

        .lower()

    )


    df = load_dataset(

        country

    )



    (

        X_train,

        X_test,

        y_train,

        y_test,

        features

    ) = split_dataset(

        df

    )



    model = train_model(

        X_train,

        y_train

    )



    predictions = predict(

        model,

        X_test

    )



    mae, rmse = evaluate_model(

        y_test,

        predictions

    )



    save_results(

        country,

        mae,

        rmse,

        predictions,

        y_test,

        model,

        features

    )


    print()

    print("="*70)

    print("DONE")

    print("="*70)




# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    main()