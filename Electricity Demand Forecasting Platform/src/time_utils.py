import pandas as pd


def convert_to_utc(
    df,
    datetime_col="datetime",
    timezone="Europe/Berlin"
):
    """
    Convert timestamps to UTC.
    Handles both timezone-aware and timezone-naive data.
    """

    df = df.copy()

    df[datetime_col] = pd.to_datetime(
        df[datetime_col]
    )


    # Case 1:
    # ENTSO-E already provides timezone information
    if df[datetime_col].dt.tz is not None:

        df[datetime_col] = (
            df[datetime_col]
            .dt.tz_convert("UTC")
            .dt.tz_localize(None)
        )


    # Case 2:
    # Dataset has no timezone information
    else:

        df[datetime_col] = (
            df[datetime_col]
            .dt.tz_localize(
                timezone,
                ambiguous="NaT",
                nonexistent="shift_forward"
            )
            .dt.tz_convert("UTC")
            .dt.tz_localize(None)
        )

        df = df.dropna(
            subset=[datetime_col]
        )


    return df