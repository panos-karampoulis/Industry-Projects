COUNTRIES = {

    "germany": {

        "enabled": True,

        "country_code": "DE",

        "domain": "10Y1001A1001A82H",

        "timezone": "Europe/Berlin",

        "datasets": {
            "load": "15min",
            "prices": "60min",
             "generation": "60min"
        }

    },


    "france": {

        "enabled":  True,

        "country_code": "FR",

        "domain": "10YFR-RTE------C",

        "timezone": "Europe/Paris",

        "datasets": {
            "load": "15min",
            "prices": "60min",
             "generation": "60min"
        }

    },


    "italy": {

        "enabled": True,

        "country_code": "IT",

        "domain": "10Y1001A1001A70O",

        "timezone": "Europe/Rome",

        "datasets": {
            "load": "15min",
            "prices": "60min",
             "generation": "60min"
        }

    },


    "netherlands": {

        "enabled":  True,

        "country_code": "NL",

        "domain": "10YNL----------L",

        "timezone": "Europe/Amsterdam",

        "datasets": {
            "load": "15min",
            "prices": "60min",
             "generation": "60min"
        }

    },


    "spain": {

        "enabled":  True,

        "country_code": "ES",

        "domain": "10YES-REE------0",

        "timezone": "Europe/Madrid",

        "datasets": {
            "load": "15min",
            "prices": "60min",
             "generation": "60min"
        }

    }

}

# ==========================================================
# ACTIVE COUNTRIES
# ==========================================================

def get_active_countries():

    return [

        country

        for country, config

        in COUNTRIES.items()

        if config["enabled"]

    ]


# ==========================================================
# COUNTRY CONFIG
# ==========================================================

def get_country_config(country):

    return COUNTRIES[country]