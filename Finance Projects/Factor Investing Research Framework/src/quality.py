import pandas as pd


def calculate_quality(
    fundamentals
):

    quality = (
        fundamentals
        .sort_values(
            "ROE",
            ascending=False
        )
    )

    return quality