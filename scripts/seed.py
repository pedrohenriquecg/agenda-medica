from app.database import get_connection
from werkzeug.security import generate_password_hash


def main() -> None:
    connection = get_connection()
    password_hash = generate_password_hash("admin123")

    try:
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

    finally:
        connection.close()


if __name__ == "__main__":
    main()
