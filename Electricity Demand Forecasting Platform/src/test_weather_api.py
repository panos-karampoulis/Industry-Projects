from weather_forecast_api import get_future_weather


weather = get_future_weather(

    latitude=52.52,

    longitude=13.405,

    forecast_date="2026-07-24"

)


print(weather.head())

print()

print(weather.shape)

print()

print(weather.tail())