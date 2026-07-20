from app.database import get_connection


def create_user(username: str, password: str) -> None:
    connection = get_connection()

    try:
        connection.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password),
        )
        connection.commit()
    finally:
        connection.close()


def validate_user(username: str, password: str) -> bool:
    connection = get_connection()

    try:
        user = connection.execute(
            "SELECT 1 FROM users WHERE username = ? AND password = ? LIMIT 1",
            (username, password),
        ).fetchone()

        return user is not None
    finally:
        connection.close()
