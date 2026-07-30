import pandas as pd
import numpy as np
import os
import argparse
import pickle
import warnings


from catboost import CatBoostRegressor


from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error
)


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

        f"models/{country}/catboost_model.pkl"

    )


    result_path = (

        f"results/{country}/catboost_results.csv"

    )


    prediction_path = (

        f"results/{country}/catboost_predictions.csv"

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
# LOAD DATASET
# ============================================================

def load_dataset(country):


    (

        feature_file,

        _,

        _,

        _

    ) = get_paths(country)



    print("="*70)

    print("CATBOOST FORECASTING")

    print("="*70)


    print()

    print(

        "Country:",

        country

    )


    print()


    print(

        "Loading:",

        feature_file

    )


    df = pd.read_csv(

        feature_file,

        index_col=0,

        parse_dates=True

    )


    df = df.sort_index()


    print()

    print(

        "Dataset:"

    )


    print(

        df.shape

    )


    return df




# ============================================================
# TRAIN TEST SPLIT
# ============================================================

def split_dataset(df):


    target = "price_eur_mwh"



    features = [

        col

        for col in df.columns

        if col != target

    ]



    X = df[features]


    y = df[target]



    split = int(

        len(df)*0.80

    )



    X_train = X.iloc[:split]


    X_test = X.iloc[split:]



    y_train = y.iloc[:split]


    y_test = y.iloc[split:]



    print()


    print(

        "Train:"

    )


    print(

        X_train.shape

    )



    print()


    print(

        "Test:"

    )


    print(

        X_test.shape

    )



    return (

        X_train,

        X_test,

        y_train,

        y_test,

        features

    )




# ============================================================
# TRAIN CATBOOST
# ============================================================

def train_model(

    X_train,

    y_train

):


    print()


    print(

        "Training CatBoost..."

    )



    model = CatBoostRegressor(


        iterations=500,


        learning_rate=0.05,


        depth=8,


        loss_function="RMSE",


        random_seed=42,


        verbose=100


    )



    model.fit(

        X_train,

        y_train

    )



    print()


    print(

        "Training completed"

    )



    return model




# ============================================================
# PREDICT
# ============================================================

def predict(

    model,

    X_test

):


    print()


    print(

        "Creating predictions..."

    )



    predictions = model.predict(

        X_test

    )



    return predictions

# ============================================================
# EVALUATION
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

def feature_importance(

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
# SAVE OUTPUTS
# ============================================================

def save_outputs(

    country,

    model,

    mae,

    rmse,

    y_test,

    predictions,

    features

):


    (

        _,

        model_path,

        result_path,

        prediction_path

    ) = get_paths(country)




    # -------------------------
    # Save model
    # -------------------------

    with open(

        model_path,

        "wb"

    ) as f:


        pickle.dump(

            model,

            f

        )



    # -------------------------
    # Metrics
    # -------------------------

    results = pd.DataFrame({

        "model":[

            "CatBoost"

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
    # Predictions
    # -------------------------

    prediction_df = pd.DataFrame({

        "actual":

            y_test,


        "catboost_prediction":

            predictions

    })



    prediction_df.to_csv(

        prediction_path

    )



    # -------------------------
    # Feature importance
    # -------------------------

    importance = feature_importance(

        model,

        features

    )


    importance.to_csv(

        f"results/{country}/catboost_feature_importance.csv",

        index=False

    )




    print()

    print("Saved:")

    print(model_path)

    print(result_path)

    print(prediction_path)






# ============================================================
# MAIN PIPELINE
# ============================================================

def main():


    args = parse_arguments()


    country = args.country.lower()



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



    save_outputs(

        country,

        model,

        mae,

        rmse,

        y_test,

        predictions,

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