import requests
import pandas as pd
from pathlib import Path
import time


# =====================================
# Configuration
# =====================================

OUTPUT_FOLDER = Path("../data/raw/smard_generation")

OUTPUT_FOLDER.mkdir(
    parents=True,
    exist_ok=True
)


DATASETS = {
    "solar": 4068,
    "wind_onshore": 4067,
    "wind_offshore": 1225
}


# =====================================
# Get available chunks
# =====================================

def get_timestamps(chart_id):

    url = (
        f"https://www.smard.de/app/chart_data/"
        f"{chart_id}/DE/index_hour.json"
    )

    print(
        "Getting index:",
        chart_id
    )


    response = requests.get(url)

    response.raise_for_status()


    data = response.json()


    timestamps = data["timestamps"]


    print(
        "Chunks found:",
        len(timestamps)
    )


    return timestamps



# =====================================
# Download dataset
# =====================================

def download_dataset(dataset_name, chart_id):

    print("\n====================")
    print("Downloading:", dataset_name)
    print("====================")


    timestamps = get_timestamps(chart_id)


    all_data = []


    for i, timestamp in enumerate(timestamps):

        url = (
            f"https://www.smard.de/app/chart_data/"
            f"{chart_id}/DE/"
            f"{chart_id}_DE_hour_{timestamp}.json"
        )


        print(
            f"{i+1}/{len(timestamps)}"
        )


        response = requests.get(url)


        if response.status_code != 200:

            print(
                "Failed:",
                response.status_code
            )

            continue


        data = response.json()


        if "series" not in data:

            print(
                "Missing series"
            )

            continue


        df = pd.DataFrame(
            data["series"],
            columns=[
                "timestamp",
                dataset_name
            ]
        )


        all_data.append(df)


        time.sleep(0.15)



    if not all_data:

        print(
            "No data downloaded"
        )

        return



    final = pd.concat(
        all_data,
        ignore_index=True
    )


    final["datetime"] = pd.to_datetime(
        final["timestamp"],
        unit="ms"
    )


    final = final[
        [
            "datetime",
            dataset_name
        ]
    ]


    final = final.drop_duplicates(
        subset="datetime"
    )


    final = final.sort_values(
        "datetime"
    )


    output_file = (
        OUTPUT_FOLDER /
        f"{dataset_name}.csv"
    )


    final.to_csv(
        output_file,
        index=False
    )


    print()
    print(
        "Saved:",
        output_file
    )

    print(
        "Rows:",
        len(final)
    )



# =====================================
# Main
# =====================================

if __name__ == "__main__":


    for name, chart_id in DATASETS.items():

        download_dataset(
            name,
            chart_id
        )