import subprocess
import sys


COUNTRIES = [
    "germany",
    "france",
    "italy",
    "spain",
    "netherlands"
]


for country in COUNTRIES:

    print("\n" + "="*60)
    print(f"TRAINING LOAD FORECAST MODEL: {country.upper()}")
    print("="*60)


    subprocess.run(
        [
            sys.executable,
            "src/risk/generate_load_forecast.py",
            country
        ]
    )


print("\nALL LOAD FORECAST MODELS COMPLETED")