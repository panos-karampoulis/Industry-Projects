from pathlib import Path
import json


BASE_DIR = Path(__file__).resolve().parent.parent


CONFIG_PATH = (
    BASE_DIR
    / "config"
    / "countries.json"
)


def load_country_config():

    with open(CONFIG_PATH, "r") as f:
        return json.load(f)