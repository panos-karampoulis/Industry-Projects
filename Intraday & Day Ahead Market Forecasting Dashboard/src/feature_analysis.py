import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path



# ============================================================
# PATHS
# ============================================================


BASE_DIR = Path(__file__).resolve().parents[2]


IMPORTANCE_FILE = (
    BASE_DIR
    /
    "data"
    /
    "results"
    /
    "feature_importance.csv"
)


OUTPUT_DIR = (

    BASE_DIR
    /
    "images"
    /
    "feature_importance"

)


OUTPUT_DIR.mkdir(
    exist_ok=True,
    parents=True
)




# ============================================================
# LOAD DATA
# ============================================================


print("="*60)

print(
    "Loading feature importance"
)

print("="*60)



df = pd.read_csv(

    IMPORTANCE_FILE

)



print(
    df.head()
)


print(
    df.shape
)




# ============================================================
# GLOBAL FEATURE IMPORTANCE
# ============================================================


global_importance = (

    df

    .groupby(
        "feature"
    )

    ["importance"]

    .mean()

    .sort_values(
        ascending=False
    )

)



global_file = (

    OUTPUT_DIR

    /
    "global_feature_importance.csv"

)



global_importance.to_csv(

    global_file

)



print()

print(
    "Top Features"
)

print(
    global_importance.head(15)
)



# ============================================================
# GLOBAL PLOT
# ============================================================



plt.figure(
    figsize=(10,6)
)



global_importance.head(15).sort_values().plot(

    kind="barh"

)



plt.title(

    "Global Feature Importance"

)


plt.xlabel(

    "Importance"

)



plt.tight_layout()



plt.savefig(

    OUTPUT_DIR
    /
    "global_feature_importance.png",

    dpi=300

)



plt.close()





# ============================================================
# COUNTRY LEVEL ANALYSIS
# ============================================================


countries = (

    df["country"]

    .unique()

)



for country in countries:



    print()

    print(
        "Processing:",
        country
    )



    country_df = (

        df[
            df["country"]
            ==
            country
        ]

        .groupby(
            "feature"
        )

        ["importance"]

        .mean()

        .sort_values(
            ascending=False
        )

    )



    print(
        country_df.head(10)
    )



    country_df.to_csv(

        OUTPUT_DIR

        /

        f"{country}_importance.csv"

    )



    plt.figure(

        figsize=(10,6)

    )



    country_df.head(15).sort_values().plot(

        kind="barh"

    )



    plt.title(

        f"{country.upper()} Feature Importance"

    )



    plt.xlabel(

        "Importance"

    )



    plt.tight_layout()



    plt.savefig(

        OUTPUT_DIR

        /

        f"{country}_feature_importance.png",

        dpi=300

    )



    plt.close()




# ============================================================
# FINISH
# ============================================================


print()

print("="*60)

print(
    "FEATURE ANALYSIS COMPLETED"
)

print("="*60)



print(

    "Saved:",
    OUTPUT_DIR

)