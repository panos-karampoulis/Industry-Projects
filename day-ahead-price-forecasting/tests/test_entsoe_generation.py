import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

sys.path.append(
    str(BASE_DIR / "src")
)


import pandas as pd

from data.entsoe_loader import EntsoeLoader


loader = EntsoeLoader()


start = pd.Timestamp(
    "2026-07-01",
    tz="Europe/Berlin"
)

end = pd.Timestamp(
    "2026-07-02",
    tz="Europe/Berlin"
)


generation = loader.get_generation(
    "DE_LU",
    start,
    end
)


print("\nGeneration data:")
print(generation.head())


print("\nShape:")
print(generation.shape)


print("\nColumns:")
print(generation.columns.tolist())