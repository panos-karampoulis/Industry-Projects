import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]

sys.path.append(
    str(BASE_DIR)
)




from entsoe import EntsoePandasClient

from config import API_KEY


client = EntsoePandasClient(

    api_key=API_KEY

)