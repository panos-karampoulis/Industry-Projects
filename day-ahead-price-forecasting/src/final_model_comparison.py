import pandas as pd
import matplotlib.pyplot as plt
import os
import argparse


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

    results_path = (
        f"results/{country}"
    )

    return results_path



# ============================================================
# LOAD RESULTS
# ============================================================

def load_metrics(country):


    folder = get_paths(country)


    models = [

        "random_forest",

        "xgboost",

        "lightgbm",

        "catboost"

    ]


    all_results = []


    for model in models:


        file = (

            f"{folder}/"
            f"{model}_results.csv"

        )


        if os.path.exists(file):


            df = pd.read_csv(file)


            all_results.append(df)



    comparison = pd.concat(

        all_results,

        ignore_index=True

    )


    return comparison




# ============================================================
# BAR CHART
# ============================================================

def create_chart(

    comparison,

    country

):


    plt.figure(

        figsize=(10,6)

    )


    plt.bar(

        comparison["model"],

        comparison["MAE"]

    )


    plt.title(

        f"{country.upper()} - MAE Comparison"

    )


    plt.ylabel(

        "MAE (€/MWh)"

    )


    plt.xticks(

        rotation=45

    )


    plt.tight_layout()


    output = (

        f"results/{country}/"
        "model_comparison_mae.png"

    )


    plt.savefig(

        output,

        dpi=300

    )


    plt.close()



    print()

    print(

        "Saved chart:"

    )

    print(output)




# ============================================================
# PREDICTION COMPARISON
# ============================================================

def load_predictions(country):


    folder = get_paths(country)


    files = {

        "Random Forest":

        "random_forest_predictions.csv",


        "XGBoost":

        "xgboost_predictions.csv",


        "LightGBM":

        "lightgbm_predictions.csv",


        "CatBoost":

        "catboost_predictions.csv"

    }



    comparison = None



    for name,file in files.items():


        path = (

            f"{folder}/{file}"

        )


        if os.path.exists(path):


            df = pd.read_csv(

                path,

                index_col=0,

                parse_dates=True

            )


            pred_col = [

                c for c in df.columns

                if c != "actual"

            ][0]



            df = df.rename(

                columns={

                    pred_col:name

                }

            )



            if comparison is None:


                comparison = df



            else:


                comparison = comparison.join(

                    df[name],

                    how="inner"

                )



    return comparison




# ============================================================
# FORECAST PLOT
# ============================================================

def forecast_plot(

    predictions,

    country

):


    plt.figure(

        figsize=(14,6)

    )


    sample = predictions.iloc[:168]


    plt.plot(

        sample["actual"],

        label="Actual"

    )


    for col in predictions.columns:


        if col != "actual":

            plt.plot(

                sample[col],

                label=col

            )



    plt.title(

        f"{country.upper()} - Forecast Comparison (1 Week)"

    )


    plt.ylabel(

        "€/MWh"

    )


    plt.legend()


    plt.tight_layout()



    output = (

        f"results/{country}/"
        "forecast_comparison_week.png"

    )


    plt.savefig(

        output,

        dpi=300

    )


    plt.close()



    print()

    print(

        "Saved:"

    )

    print(output)




# ============================================================
# MAIN
# ============================================================

def main():


    args = parse_arguments()


    country = args.country.lower()



    print("="*70)

    print("FINAL MODEL COMPARISON")

    print("="*70)



    metrics = load_metrics(

        country

    )


    print()

    print(metrics)



    print()

    print(

        "BEST MODEL"

    )


    best = metrics.sort_values(

        "MAE"

    ).iloc[0]


    print(best)



    create_chart(

        metrics,

        country

    )



    predictions = load_predictions(

        country

    )


    if predictions is not None:


        print()

        print(

            predictions.head()

        )


        forecast_plot(

            predictions,

            country

        )



    print()

    print("DONE")



if __name__ == "__main__":

    main()