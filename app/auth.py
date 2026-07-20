import sqlite3

from werkzeug.security import check_password_hash, generate_password_hash

from app.database import get_connection


class AuthenticationDatabaseError(Exception):
    pass


def create_user(username: str, password: str) -> None:
    connection: sqlite3.Connection | None = None
    password_hash = generate_password_hash(password)

    try:
        connection = get_connection()
        connection.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password_hash),
        )
        connection.commit()
    except sqlite3.Error as error:
        raise AuthenticationDatabaseError(
            "Erro ao acessar o banco de dados de autenticação."
        ) from error
    finally:
        if connection is not None:
            connection.close()


def validate_user(username: str, password: str) -> bool:
    connection: sqlite3.Connection | None = None

    try:
        connection = get_connection()
        user = connection.execute(
            "SELECT password FROM users WHERE username = ? LIMIT 1",
            (username,),
        ).fetchone()

        if user is None:
            return False

        return check_password_hash(user["password"], password)
    except sqlite3.Error as error:
        raise AuthenticationDatabaseError(
            "Erro ao acessar o banco de dados de autenticação."
        ) from error
    finally:
        if connection is not None:
            connection.close()
