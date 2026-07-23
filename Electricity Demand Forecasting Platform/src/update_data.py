import argparse


from download_load import download_load
from download_weather import download_weather
from prepare_dataset import prepare_dataset




def update_country(country):


    print("====================")
    print(
        f"Updating {country}"
    )
    print("====================")


    download_load(
        country
    )


    download_weather(
        country
    )


    dataset = prepare_dataset(
        country
    )


    print()

    print(
        "UPDATE COMPLETED"
    )

    print(dataset)





if __name__ == "__main__":


    parser = argparse.ArgumentParser()


    parser.add_argument(
        "--country",
        required=True
    )


    args = parser.parse_args()


    update_country(
        args.country
    )