from src.config.settings import (
    HISTORICAL_START_DATE,
    get_current_date
)


from src.config.countries import (
    get_active_countries,
    get_country_config
)



print(
    "Historical start:"
)

print(
    HISTORICAL_START_DATE
)



print(
    "\nCurrent date:"
)

print(
    get_current_date()
)



print(
    "\nActive countries:"
)

print(
    get_active_countries()
)



print(
    "\nGermany config:"
)

print(
    get_country_config(
        "germany"
    )
)