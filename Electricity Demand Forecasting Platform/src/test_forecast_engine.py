from forecast_engine import generate_forecast



forecast, summary = generate_forecast(

    country="france"

)



print(
    forecast.head()
)


print()

print(
    "Rows:",
    len(forecast)
)


print()

print("======================")
print("Forecast Summary")
print("======================")


for key, value in summary.items():

    print(
        key,
        ":",
        value
    )