from src.data_loader.entsoe_client import EntsoeClient


client = EntsoeClient()


df = client.get_load_data(
    country="germany",
    start="2026-01-01",
    end="2026-01-05"
)


print(df.head())

print(
    df.shape
)