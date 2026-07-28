import pandas as pd
import numpy as np
import joblib
import shap
import matplotlib.pyplot as plt


from pathlib import Path



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


MODEL_DIR = (
    BASE_DIR
    /
    "models"
)


OUTPUT_DIR = (
    BASE_DIR
    /
    "images"
    /
    "shap"
)


OUTPUT_DIR.mkdir(
    exist_ok=True,
    parents=True
)



# ============================================================
# SETTINGS
# ============================================================


COUNTRIES = [

    "france",
    "germany",
    "italy",
    "netherlands",
    "spain"

]



TARGET = "price_eur_mwh"




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





# ============================================================
# COUNTRY LOOP
# ============================================================


for country in COUNTRIES:


    print("\n")

    print("="*60)

    print(
        country.upper()
    )

    print("="*60)



    country_df = (

        df[
            df["country"]
            ==
            country

        ]

        .sort_values(
            "timestamp"
        )

        .copy()

    )



    # --------------------------------------------------------
    # MODEL PATH
    # --------------------------------------------------------


    model_path = (

        MODEL_DIR

        /

        country

        /

        "Linear_Regression.joblib"

    )



    if not model_path.exists():

        print(
            "Model missing:",
            model_path
        )

        continue



    model = joblib.load(

        model_path

    )



    print(
        "Loaded model:",
        model_path
    )




    # --------------------------------------------------------
    # FEATURES
    # --------------------------------------------------------


    X = country_df.drop(

        columns=[
            TARGET
        ],

        errors="ignore"

    )



    # Keep only numeric columns

    X = X.select_dtypes(

        include=[
            "number"
        ]

    )



    # Match training features exactly

    model_features = model.feature_names_in_



    X = X[model_features]



    print(
        "SHAP input:",
        X.shape
    )



    print(
        X.columns.tolist()
    )




    # --------------------------------------------------------
    # TEST SPLIT
    # --------------------------------------------------------


    split = int(

        len(X)
        *
        0.8

    )



    X_test = X.iloc[split:]




    # sample for speed

    X_sample = (

        X_test

        .sample(

            n=min(
                300,
                len(X_test)
            ),

            random_state=42

        )

    )



    print(
        "Sample:",
        X_sample.shape
    )





    # --------------------------------------------------------
    # SHAP
    # --------------------------------------------------------


    print(
        "Calculating SHAP..."
    )



    explainer = shap.Explainer(

        model.predict,

        X_sample

    )



    shap_values = explainer(

        X_sample

    )




    # --------------------------------------------------------
    # SUMMARY PLOT
    # --------------------------------------------------------


    plt.figure(

        figsize=(10,6)

    )


    shap.summary_plot(

        shap_values,

        X_sample,

        show=False

    )



    plt.title(

        f"{country.upper()} SHAP Feature Impact"

    )



    plt.tight_layout()



    plt.savefig(

        OUTPUT_DIR

        /

        f"{country}_shap_summary.png",

        dpi=300,

        bbox_inches="tight"

    )


    plt.close()





    # --------------------------------------------------------
    # SHAP IMPORTANCE CSV
    # --------------------------------------------------------


    shap_importance = pd.DataFrame(

        {

            "feature":

            X_sample.columns,


            "mean_abs_shap":

            np.abs(
                shap_values.values
            )

            .mean(
                axis=0
            )

        }

    )



    shap_importance = (

        shap_importance

        .sort_values(

            "mean_abs_shap",

            ascending=False

        )

    )



    shap_importance.to_csv(

        OUTPUT_DIR

        /

        f"{country}_shap_importance.csv",

        index=False

    )



    print()

    print(
        "Top SHAP Features:"
    )

    print(

        shap_importance.head(10)

    )






print("\n")

print("="*60)

print(
    "SHAP ANALYSIS COMPLETED"
)

print("="*60)


print(

    "Saved:",
    OUTPUT_DIR

)