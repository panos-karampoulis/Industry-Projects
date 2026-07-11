import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from sqlalchemy import create_engine
from config.config import DB_CONFIG


def get_engine():

    connection_string = (
        f"mysql+pymysql://"
        f"{DB_CONFIG['user']}:"
        f"{DB_CONFIG['password']}@"
        f"{DB_CONFIG['host']}/"
        f"{DB_CONFIG['database']}"
    )

    engine = create_engine(connection_string)

    return engine


print("Database engine created successfully")