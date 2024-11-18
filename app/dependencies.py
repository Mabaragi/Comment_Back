# dependencies.py
from .services.database import MongoDB

mongo: dict[str, MongoDB] = {}


def get_database() -> dict[str, MongoDB]:
    return mongo
