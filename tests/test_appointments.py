from requests import RequestException

import app.routes as routes


def test_mock_api_returns_required_appointments(client, required_appointment_fields):
    response = client.get("/api/appointments")
    data = response.get_json()

    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) == 6
    assert all(required_appointment_fields <= set(item) for item in data)


def test_agenda_renders_table_structure_with_valid_data(
    monkeypatch,
    authenticated_client,
    sample_appointments,
):
    monkeypatch.setattr(
        routes,
        "fetch_appointments",
        lambda api_url, timeout: sample_appointments,
    )

    response = authenticated_client.get("/agenda")
    response_text = response.get_data(as_text=True)

    assert response.status_code == 200
    assert 'id="appointments-table"' in response_text
    assert 'id="appointments-data"' in response_text
    assert "Ana Souza" in response_text
    assert "tabulator.min.js" in response_text
    assert "agenda.js" in response_text
    assert "Não foi possível carregar os agendamentos." not in response_text


def test_agenda_handles_unavailable_api(monkeypatch, authenticated_client):
    def raise_request_error(api_url, timeout):
        raise RequestException("api unavailable")

    monkeypatch.setattr(routes, "fetch_appointments", raise_request_error)

    response = authenticated_client.get("/agenda")
    response_text = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "Não foi possível carregar os agendamentos." in response_text
    assert 'id="appointments-table"' in response_text


def test_agenda_handles_invalid_api_response(monkeypatch, authenticated_client):
    def raise_value_error(api_url, timeout):
        raise ValueError("technical validation message")

    monkeypatch.setattr(routes, "fetch_appointments", raise_value_error)

    response = authenticated_client.get("/agenda")
    response_text = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "Não foi possível carregar os agendamentos." in response_text
    assert "technical validation message" not in response_text


def test_agenda_handles_empty_appointment_list(monkeypatch, authenticated_client):
    monkeypatch.setattr(routes, "fetch_appointments", lambda api_url, timeout: [])

    response = authenticated_client.get("/agenda")
    response_text = response.get_data(as_text=True)

    assert response.status_code == 200
    assert 'id="appointments-table"' in response_text
    assert 'id="appointments-message"' in response_text
    assert "[]" in response_text
