import pandas as pd



def validate_dataframe(
    df,
    name="dataset"
):

    print("\n")
    print("=" * 60)
    print(f"VALIDATION REPORT: {name}")
    print("=" * 60)



    # -------------------------------------------------
    # Shape
    # -------------------------------------------------

    print(
        "Rows:",
        len(df)
    )


    print(
        "Columns:",
        list(df.columns)
    )



    # -------------------------------------------------
    # Timestamp check
    # -------------------------------------------------

    if "timestamp" in df.columns:


        df["timestamp"] = pd.to_datetime(
            df["timestamp"]
        )


        print(
            "Start:",
            df["timestamp"].min()
        )


        print(
            "End:",
            df["timestamp"].max()
        )


        print(
            "Timezone:",
            df["timestamp"].dt.tz
        )



        duplicates = (
            df["timestamp"]
            .duplicated()
            .sum()
        )


        print(
            "Duplicate timestamps:",
            duplicates
        )



        frequency = (
            df["timestamp"]
            .sort_values()
            .diff()
            .mode()
        )


        if len(frequency) > 0:

            print(
                "Detected frequency:",
                frequency.iloc[0]
            )



    else:

        print(
            "WARNING: timestamp column missing"
        )



    # -------------------------------------------------
    # Missing values
    # -------------------------------------------------

    missing = (
        df.isna()
        .sum()
    )


    missing_total = (
        missing.sum()
    )


    print(
        "Missing values:",
        missing_total
    )


    if missing_total > 0:

        print(
            missing[missing > 0]
        )



    # -------------------------------------------------
    # Numeric statistics
    # -------------------------------------------------

    print("\nNumeric summary:")


    print(
        df.describe()
    )



    print("=" * 60)

    return True