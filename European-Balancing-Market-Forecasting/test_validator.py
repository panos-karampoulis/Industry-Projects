from src.data_loader.entsoe_client import EntsoeClient

from src.data_loader.validator import (
    validate_dataframe
)



client = EntsoeClient()



df = client.get_load_data(
    country="germany",
    start="2026-01-01",
    end="2026-01-05"
)



validate_dataframe(
    df,
    name="Germany Load"
)