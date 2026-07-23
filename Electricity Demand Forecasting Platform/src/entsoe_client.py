import os

from dotenv import load_dotenv
from entsoe import EntsoePandasClient


# ----------------------------------------
# Load environment variables
# ----------------------------------------

load_dotenv()


def get_client():
    """
    Returns authenticated ENTSO-E client.
    """

    api_key = os.getenv("ENTSOE_API_KEY")

    if api_key is None:
        raise ValueError(
            "ENTSOE_API_KEY not found in .env"
        )

    return EntsoePandasClient(
        api_key=api_key
    )