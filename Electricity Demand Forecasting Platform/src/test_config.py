import yaml
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


file = (
    BASE_DIR
    /
    "configs"
    /
    "models.yaml"
)


with open(file, "r") as f:

    models = yaml.safe_load(f)


print(models)


print()

print(
    "Italy metrics:"
)

print(
    models["italy"]["metrics"]
)