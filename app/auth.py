from werkzeug.security import check_password_hash, generate_password_hash

from app.database import get_connection


def create_user(username: str, password: str) -> None:
    connection = get_connection()
    password_hash = generate_password_hash(password)

    try:
        connection.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password_hash),
        )
        connection.commit()
    finally:
        connection.close()


def validate_user(username: str, password: str) -> bool:
    connection = get_connection()

    try:
        user = connection.execute(
            "SELECT password FROM users WHERE username = ? LIMIT 1",
            (username,),
        ).fetchone()

        if user is None:
            return False

        return check_password_hash(user["password"], password)
    finally:
        connection.close()
