import sys
from pathlib import Path

# Add src folder to path
sys.path.append(
    str(Path(__file__).resolve().parents[1] / "src")
)


import pandas as pd

from data.weather_loader import WeatherLoader



loader = WeatherLoader()



start = pd.Timestamp(
    "2020-01-01"
)


end = pd.Timestamp(
    "2020-01-31"
)



weather = loader.get_weather(

    52.5200,

    13.4050,

    start,

    end

)



print(weather.head())


print(
    weather.shape
)