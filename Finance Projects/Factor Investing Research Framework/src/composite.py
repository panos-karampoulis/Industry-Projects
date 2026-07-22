import pandas as pd


def calculate_factor_score(
    momentum,
    volatility,
    quality
):

    scores = pd.DataFrame(index=momentum.index)


    # Momentum ranking
    scores["Momentum"] = (
        momentum
        .rank(pct=True)
    )


    # Quality ranking
    scores["Quality"] = (
        quality["ROE"]
        .rank(pct=True)
    )


    # Low volatility ranking
    # inverse ranking
    scores["LowVol"] = (
    1 -
    volatility
    .rank(pct=True)
    )


    scores["Composite"] = (
        0.4 * scores["Momentum"]
        +
        0.3 * scores["Quality"]
        +
        0.3 * scores["LowVol"]
    )


    return (
        scores
        .sort_values(
            "Composite",
            ascending=False
        )
    )