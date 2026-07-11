import pandas as pd


def create_summary_report(df):

    summary = {
        "Total Rows": len(df)
    }

    return pd.DataFrame(
        summary.items(),
        columns=["Metric", "Value"]
    )