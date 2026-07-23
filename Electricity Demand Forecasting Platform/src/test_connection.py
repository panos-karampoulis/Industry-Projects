import pandas as pd

from entsoe_client import get_client


client = get_client()

print("Connected successfully!")

print(client)