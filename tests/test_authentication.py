import logging
import sqlite3

import app.routes as routes
from app.auth import AuthenticationDatabaseError


def test_valid_login_redirects_to_agenda_and_stores_user(client):
    response = client.post(
        "/login",
        data={"username": "admin", "password": "admin123"},
    )

    assert response.status_code == 302
    assert response.location == "/agenda"

    with client.session_transaction() as session:
        assert session["username"] == "admin"


def test_invalid_login_shows_error_and_does_not_authenticate(client):
    response = client.post(
        "/login",
        data={"username": "admin", "password": "wrong-password"},
    )

    assert response.status_code == 200
    assert "Usuário ou senha inválidos." in response.get_data(as_text=True)

    with client.session_transaction() as session:
        assert "username" not in session


def test_agenda_requires_authentication(client):
    response = client.get("/agenda")

    assert response.status_code == 302
    assert response.location == "/login"


def test_logout_clears_session_and_protects_agenda(client):
    client.post(
        "/login",
        data={"username": "admin", "password": "admin123"},
    )

    response = client.get("/logout")

    assert response.status_code == 302
    assert response.location == "/login"

    with client.session_transaction() as session:
        assert "username" not in session

    agenda_response = client.get("/agenda")
    assert agenda_response.status_code == 302
    assert agenda_response.location == "/login"


def test_database_error_during_login_shows_friendly_message(monkeypatch, client, caplog):
    def raise_database_error(username, password):
        raise AuthenticationDatabaseError("SQLite internal error")

    monkeypatch.setattr(routes, "validate_user", raise_database_error)

    with caplog.at_level(logging.ERROR):
        response = client.post(
            "/login",
            data={"username": "admin", "password": "admin123"},
        )

    response_text = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "Não foi possível acessar o sistema no momento. Tente novamente mais tarde." in response_text
    assert "SQLite internal error" not in response_text
    assert any(
        "Erro ao acessar o banco de dados durante login." in record.message
        for record in caplog.records
    )


def test_test_database_stores_password_hash(database_path):
    connection = sqlite3.connect(database_path)

    try:
        password = connection.execute(
            "SELECT password FROM users WHERE username = ?",
            ("admin",),
        ).fetchone()[0]
    finally:
        connection.close()

    assert password != "admin123"
    assert password.startswith(("scrypt:", "pbkdf2:"))
