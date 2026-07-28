import sys
from pathlib import Path


# ============================================================
# PROJECT PATH SETUP
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

sys.path.append(
    str(BASE_DIR)
)

sys.path.append(
    str(BASE_DIR / "src")
)




import pandas as pd

from datetime import datetime

from src.data.entsoe_client import client

from config import COUNTRIES


start = pd.Timestamp(

    "2025-01-01",

    tz="Europe/Brussels"

)

end = pd.Timestamp(

    "2025-01-03",

    tz="Europe/Brussels"

)


for country, code in COUNTRIES.items():

    print("=" * 60)

    print(country.upper())

    print(code)

    print("=" * 60)

    try:

        load = client.query_load(

            code,

            start=start,

            end=end

        )

        print("✅ Load available")

        print(load.head())

    except Exception as e:

        print("❌ Load not available")

        print(e)

    print()

    # ============================================================
    # DAY AHEAD PRICES
    # ============================================================

    try:

        prices = client.query_day_ahead_prices(

            code,

            start=start,

            end=end

        )

        print("✅ Day Ahead prices available")

        print(prices.head())


    except Exception as e:

        print("❌ Day Ahead prices not available")

        print(e)


    # ============================================================
    # GENERATION
    # ============================================================

    try:

        generation = client.query_generation(

            code,

            start=start,

            end=end

        )

        print("✅ Generation available")

        print(generation.head())


    except Exception as e:

        print("❌ Generation not available")

        print(e)







    # ============================================================
    # INTRADAY PRICES
    # ============================================================

    try:

        intraday = client.query_intraday_prices(

            code,

            start=start,

            end=end,

            sequence=2

        )

        print("✅ Intraday prices available")

        print(intraday.head())


    except Exception as e:

        print("❌ Intraday prices not available")

        print(e)