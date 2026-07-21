import sqlite3
import sys

from app.database import DATABASE_PATH, get_connection
from werkzeug.security import generate_password_hash


class DatabaseInitializationError(Exception):
    pass


def initialize_database() -> None:
    connection: sqlite3.Connection | None = None
    password_hash = generate_password_hash("admin123")

    try:
        DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
        connection = get_connection()
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
            """
        )
        connection.execute(
            "INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)",
            ("admin", password_hash),
        )
        connection.commit()
    except (OSError, sqlite3.Error) as error:
        raise DatabaseInitializationError(
            "Erro ao inicializar o banco de dados SQLite."
        ) from error
    finally:
        if connection is not None:
            connection.close()


def main() -> int:
    try:
        initialize_database()
    except DatabaseInitializationError as error:
        print(error, file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
