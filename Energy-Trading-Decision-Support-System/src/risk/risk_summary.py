import os
import pandas as pd


# ==============================
# Paths
# ==============================

RISK_PATH = "data/risk"

OUTPUT_PATH = (
    "data/risk/risk_summary.csv"
)


COUNTRIES = [
    "germany",
    "france",
    "italy",
    "spain",
    "netherlands"
]


# ==============================
# Process Country
# ==============================

def summarize_country(country):


    file_path = os.path.join(
        RISK_PATH,
        f"{country}_imbalance_risk.csv"
    )


    print(
        "\nProcessing:",
        country.upper()
    )


    df = pd.read_csv(
        file_path
    )


    summary = {

        "country":
            country.upper(),


        "rows":
            len(df),


        "avg_risk_score":
            df["risk_score"].mean(),


        "max_risk_score":
            df["risk_score"].max(),


        "avg_imbalance_mw":
            df["imbalance_mw"].mean(),


        "max_abs_imbalance_mw":
            df["imbalance_mw"]
            .abs()
            .max(),


        "high_risk_events":
            df["high_risk_event"]
            .sum(),


        "medium_risk_events":
            (
                df["risk_level"]
                ==
                "MEDIUM"
            )
            .sum(),


        "high_risk_percentage":
            (
                df["high_risk_event"]
                .mean()
                *
                100
            )

    }


    return summary



# ==============================
# Main
# ==============================

def main():


    summaries = []


    for country in COUNTRIES:

        summaries.append(
            summarize_country(country)
        )


    summary_df = pd.DataFrame(
        summaries
    )


    os.makedirs(
        RISK_PATH,
        exist_ok=True
    )


    summary_df.to_csv(
        OUTPUT_PATH,
        index=False
    )


    print("\n")
    print("="*60)
    print("RISK SUMMARY CREATED")
    print("="*60)


    print(
        summary_df
        .round(2)
        .to_string(
            index=False
        )
    )


    print("\nSaved:")
    print(
        OUTPUT_PATH
    )



if __name__ == "__main__":
    main()