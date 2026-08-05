import os
import pandas as pd


# ==============================
# Paths
# ==============================

INPUT_PATH = (
    "data/risk/risk_summary.csv"
)


OUTPUT_DIR = (
    "data/decision"
)


OUTPUT_PATH = (
    "data/decision/trading_decision_report.csv"
)



# ==============================
# Risk Classification
# ==============================

def classify_risk(score):

    if score < 15:
        return "LOW"

    elif score < 25:
        return "MEDIUM"

    else:
        return "HIGH"



# ==============================
# Trading Recommendation
# ==============================

def generate_action(row):


    risk = row["risk_category"]


    if risk == "LOW":

        return (
            "Increase exposure - "
            "normal trading operation"
        )


    elif risk == "MEDIUM":

        return (
            "Maintain exposure - "
            "monitor imbalance conditions"
        )


    else:

        return (
            "Reduce exposure - "
            "increase balancing reserve"
        )



# ==============================
# Exposure Score
# ==============================

def calculate_exposure_score(risk_score):

    """
    100 = safest market
    0 = highest risk
    """

    score = 100 - (
        risk_score * 2
    )


    return max(
        0,
        min(
            100,
            score
        )
    )



# ==============================
# Confidence Score
# ==============================

def calculate_confidence(row):


    risk = row["risk_category"]


    high_events = row[
        "high_risk_events"
    ]


    if risk == "LOW":

        confidence = 85


    elif risk == "MEDIUM":

        confidence = 75


    else:

        confidence = 60


    # penalty for frequent extreme events

    if high_events > 100:

        confidence -= 10


    return max(
        confidence,
        0
    )



# ==============================
# Main Engine
# ==============================

def main():


    print(
        "Loading risk summary..."
    )


    df = pd.read_csv(
        INPUT_PATH
    )


    print(
        "Generating trading decisions..."
    )


    # Risk category

    df[
        "risk_category"
    ] = (
        df[
            "avg_risk_score"
        ]
        .apply(
            classify_risk
        )
    )


    # Trading action

    df[
        "recommended_action"
    ] = (
        df.apply(
            generate_action,
            axis=1
        )
    )


    # Exposure score

    df[
        "exposure_score"
    ] = (
        df[
            "avg_risk_score"
        ]
        .apply(
            calculate_exposure_score
        )
    )


    # Confidence

    df[
        "confidence_score"
    ] = (
        df.apply(
            calculate_confidence,
            axis=1
        )
    )


    # Ranking

    df[
        "market_rank"
    ] = (
        df[
            "avg_risk_score"
        ]
        .rank(
            method="dense"
        )
        .astype(int)
    )


    # Sort safest first

    df = df.sort_values(
        "market_rank"
    )


    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )


    df.to_csv(
        OUTPUT_PATH,
        index=False
    )


    print("\n")
    print("="*60)
    print(
        "TRADING DECISION REPORT CREATED"
    )
    print("="*60)


    print(
        df[
            [
                "country",
                "avg_risk_score",
                "risk_category",
                "recommended_action",
                "exposure_score",
                "confidence_score"
            ]
        ]
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