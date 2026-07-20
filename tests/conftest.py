import sqlite3

import pytest
from werkzeug.security import generate_password_hash

from app import create_app
from app import database


@pytest.fixture
def database_path(tmp_path, monkeypatch):
    path = tmp_path / "agenda_test.db"
    monkeypatch.setattr(database, "DATABASE_PATH", path)

    connection = sqlite3.connect(path)
    try:
        connection.execute(
            """
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
            """
        )
        connection.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            ("admin", generate_password_hash("admin123")),
        )
        connection.commit()
    finally:
        connection.close()

    return path


@pytest.fixture
def app(database_path):
    flask_app = create_app()
    flask_app.config.update(
        TESTING=True,
        SECRET_KEY="test-secret-key",
        APPOINTMENTS_API_URL="http://test.local/api/appointments",
        APPOINTMENTS_API_TIMEOUT=1,
    )

    return flask_app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def authenticated_client(client):
    with client.session_transaction() as session:
        session["username"] = "admin"

    return client


@pytest.fixture
def required_appointment_fields():
    return {
        "patient",
        "cpf",
        "doctor",
        "specialty",
        "date",
        "time",
        "insurance",
        "status",
    }


@pytest.fixture
def sample_appointments():
    return [
        {
            "id": 1,
            "patient": "Ana Souza",
            "cpf": "123.456.789-00",
            "doctor": "Dr. Carlos Mendes",
            "specialty": "Cardiologia",
            "date": "2026-07-22",
            "time": "09:00",
            "insurance": "Unimed",
            "status": "Confirmado",
        }
    ]
