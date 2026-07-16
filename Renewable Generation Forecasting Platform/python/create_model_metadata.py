import json
from pathlib import Path


metadata = {

    "country": "Germany",

    "model": "XGBoost Regressor",

    "target": "renewable_total_mwh",

    "training_period": "2020-2024",

    "test_period": "2025",

    "features": 55,

    "MAE_MWh": 939.92,

    "RMSE_MWh": 1375.51,

    "R2": 0.9906
}



output_path = Path(
    "models/model_metadata.json"
)


with open(
    output_path,
    "w"
) as file:

    json.dump(
        metadata,
        file,
        indent=4
    )


print(
    "Metadata saved:",
    output_path
)