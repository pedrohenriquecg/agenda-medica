import pytest
from requests import RequestException

from app.services.appointment_api import fetch_appointments


class FakeResponse:
    def __init__(self, data, error=None):
        self.data = data
        self.error = error

    def raise_for_status(self):
        if self.error is not None:
            raise self.error

    def json(self):
        return self.data


def test_fetch_appointments_returns_valid_data(monkeypatch, sample_appointments):
    monkeypatch.setattr(
        "app.services.appointment_api.requests.get",
        lambda api_url, timeout: FakeResponse(sample_appointments),
    )

    data = fetch_appointments("http://api.test/appointments", 5)

    assert data == sample_appointments


def test_fetch_appointments_rejects_non_list_response(monkeypatch):
    monkeypatch.setattr(
        "app.services.appointment_api.requests.get",
        lambda api_url, timeout: FakeResponse({"items": []}),
    )

    with pytest.raises(ValueError):
        fetch_appointments("http://api.test/appointments", 5)


def test_fetch_appointments_rejects_non_dict_item(monkeypatch, sample_appointments):
    monkeypatch.setattr(
        "app.services.appointment_api.requests.get",
        lambda api_url, timeout: FakeResponse([sample_appointments[0], "invalid"]),
    )

    with pytest.raises(ValueError):
        fetch_appointments("http://api.test/appointments", 5)


def test_fetch_appointments_rejects_missing_required_field(monkeypatch, sample_appointments):
    invalid_appointment = dict(sample_appointments[0])
    invalid_appointment.pop("cpf")

    monkeypatch.setattr(
        "app.services.appointment_api.requests.get",
        lambda api_url, timeout: FakeResponse([invalid_appointment]),
    )

    with pytest.raises(ValueError) as error:
        fetch_appointments("http://api.test/appointments", 5)

    assert str(error.value) == "Agendamento no índice 0 sem campos obrigatórios: cpf."


def test_fetch_appointments_propagates_http_error(monkeypatch, sample_appointments):
    request_error = RequestException("request failed")

    monkeypatch.setattr(
        "app.services.appointment_api.requests.get",
        lambda api_url, timeout: FakeResponse(sample_appointments, request_error),
    )

    with pytest.raises(RequestException):
        fetch_appointments("http://api.test/appointments", 5)


def test_fetch_appointments_uses_received_url_and_timeout(monkeypatch, sample_appointments):
    call = {}

    def fake_get(api_url, timeout):
        call["api_url"] = api_url
        call["timeout"] = timeout
        return FakeResponse(sample_appointments)

    monkeypatch.setattr("app.services.appointment_api.requests.get", fake_get)

    fetch_appointments("http://api.test/appointments", 9)

    assert call == {
        "api_url": "http://api.test/appointments",
        "timeout": 9,
    }
