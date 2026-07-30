import pandas as pd
from entsoe import EntsoePandasClient


API_KEY = "8969b923-bb59-481a-8a0f-37e88bdb5527"


client = EntsoePandasClient(
    api_key=API_KEY
)


start = pd.Timestamp(
    "2025-01-01",
    tz="Europe/Brussels"
)

end = pd.Timestamp(
    "2025-01-31",
    tz="Europe/Brussels"
)


zones = {

    "IT_NORTH": "10Y1001A1001A73I",

    "IT_CENTRE_NORTH": "10Y1001A1001A70O",

    "IT_CENTRE_SOUTH": "10Y1001A1001A71M",

    "IT_SOUTH": "10Y1001A1001A788",

    "IT_SICILY": "10Y1001A1001A76J",

    "IT_SARDINIA": "10Y1001A1001A74G"

}


for name, code in zones.items():

    print("\n")
    print("="*50)
    print(name)
    print(code)
    print("="*50)


    try:

        df = client.query_day_ahead_prices(
            code,
            start=start,
            end=end
        )


        print(df.head())
        print("Shape:", df.shape)


    except Exception as e:

        print("FAILED:", e)