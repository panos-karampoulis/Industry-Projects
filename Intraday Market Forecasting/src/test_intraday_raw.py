import requests
import pandas as pd


API_KEY = "8969b923-bb59-481a-8a0f-37e88bdb5527"


params = {

    "securityToken": API_KEY,

    "documentType": "A44",

    "processType": "A01",

    "in_Domain": "10Y1001A1001A82H",

    "out_Domain": "10Y1001A1001A82H",

    "periodStart": "202501010000",

    "periodEnd": "202501020000"

}


url = (
    "https://web-api.tp.entsoe.eu/api"
)


response = requests.get(

    url,

    params=params

)


from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]


RAW_PATH = (
    BASE_DIR
    /
    "data"
    /
    "raw"
    /
    "intraday_raw.xml"
)


RAW_PATH.parent.mkdir(
    parents=True,
    exist_ok=True
)


with open(
    RAW_PATH,
    "w",
    encoding="utf-8"
) as f:

    f.write(response.text)


print(
    "Saved:",
    RAW_PATH
)




print(
    "STATUS:",
    response.status_code
)


print(
    response.text[:1000]
)