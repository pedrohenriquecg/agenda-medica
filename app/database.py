import os
import sqlite3
from pathlib import Path


DEFAULT_DATABASE_PATH = Path(__file__).resolve().parent.parent / "instance" / "agenda.db"
DATABASE_PATH = Path(os.getenv("DATABASE_PATH", str(DEFAULT_DATABASE_PATH)))


def get_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(str(DATABASE_PATH))
    connection.row_factory = sqlite3.Row
    return connection
