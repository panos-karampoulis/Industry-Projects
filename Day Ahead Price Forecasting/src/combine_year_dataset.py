import pandas as pd
from pathlib import Path
import argparse


BASE_PATH = Path("data/final")


def combine_year_dataset(country, year):

    country = country.lower()

    input_path = (
        BASE_PATH
        /
        country
        /
        str(year)
    )

    output_path = (
        input_path
        /
        f"{country}_{year}_full_dataset.csv"
    )


    print("=" * 60)
    print("Combining yearly dataset")
    print("=" * 60)

    print(f"Country: {country}")
    print(f"Year: {year}")


    monthly_files = []


    for month in range(1, 13):

        file = (
            input_path
            /
            f"{month:02d}"
            /
            "day_ahead_dataset.csv"
        )


        if file.exists():

            print(
                f"Found: {file}"
            )

            monthly_files.append(
                file
            )

        else:

            print(
                f"Missing: {file}"
            )


    if len(monthly_files) == 0:

        raise FileNotFoundError(
            "No monthly datasets found"
        )


    dfs = []


    for file in monthly_files:

        df = pd.read_csv(
            file,
            index_col="datetime"
        )


        df.index = pd.to_datetime(
            df.index
        )


        dfs.append(df)



    print()
    print("Concatenating...")


    final = pd.concat(
        dfs
    )
    # -------------------------------------------------
    # Remove duplicated columns created during concat
    # -------------------------------------------------

    final = final.loc[
        :,
        ~final.columns.duplicated()
    ]


    # Remove pandas duplicate suffix columns (.1)
    drop_columns = [
        col for col in final.columns
        if col.endswith(".1")
    ]


    if len(drop_columns) > 0:

        print(
            "Removing duplicate columns:"
        )

        print(drop_columns)

        final = final.drop(
            columns=drop_columns
        )

    # sort chronologically

    final = final.sort_index()


    # remove duplicate timestamps

    final = final[
        ~final.index.duplicated(
            keep="first"
        )
    ]


    print()
    print("Final dataset:")
    print(final.shape)


    print()
    print("Missing values:")
    print(
        final.isna().sum().sum()
    )


    final.to_csv(
        output_path
    )


    print()
    print("Saved:")
    print(output_path)



if __name__ == "__main__":


    parser = argparse.ArgumentParser()


    parser.add_argument(
        "--country",
        required=True
    )


    parser.add_argument(
        "--year",
        required=True,
        type=int
    )


    args = parser.parse_args()


    combine_year_dataset(
        args.country,
        args.year
    )