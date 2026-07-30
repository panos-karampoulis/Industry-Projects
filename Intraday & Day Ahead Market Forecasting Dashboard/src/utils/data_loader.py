import pandas as pd


def read_entsoe_csv(file):
    """
    Reads ENTSO-E CSV files regardless of header format.
    Works for:
        - single header
        - multi header
    """

    try:

        df = pd.read_csv(
            file,
            index_col=0,
            parse_dates=True
        )

        return df

    except Exception:

        pass

    # Multi-index header
    df = pd.read_csv(
        file,
        header=[0, 1],
        index_col=0,
        parse_dates=True
    )

    columns = []

    for c1, c2 in df.columns:

        if pd.isna(c2):
            columns.append(str(c1))

        else:
            columns.append(f"{c1}_{c2}")

    df.columns = columns

    return df