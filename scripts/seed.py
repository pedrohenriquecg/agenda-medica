import sqlite3
import sys

from app.database import get_connection
from werkzeug.security import generate_password_hash


class SeedDatabaseError(Exception):
    pass


def seed_database() -> None:
    connection: sqlite3.Connection | None = None
    password_hash = generate_password_hash("admin123")

    try:
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
        connection.execute(
            "UPDATE users SET password = ? WHERE username = ?",
            (password_hash, "admin"),
        )

        connection.commit()

    except sqlite3.Error as error:
        raise SeedDatabaseError("Erro ao preparar o banco de dados SQLite.") from error

    finally:
        if connection is not None:
            connection.close()


def main() -> int:
    try:
        seed_database()
    except SeedDatabaseError as error:
        print(error, file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
