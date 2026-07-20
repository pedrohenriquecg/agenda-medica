import requests


REQUIRED_APPOINTMENT_FIELDS = (
    "patient",
    "cpf",
    "doctor",
    "specialty",
    "date",
    "time",
    "insurance",
    "status",
)


def fetch_appointments(api_url: str, timeout: int) -> list[dict]:
    response = requests.get(api_url, timeout=timeout)
    response.raise_for_status()

    data = response.json()

    if not isinstance(data, list):
        raise ValueError("A API retornou um formato de dados inválido: esperado uma lista.")

    for index, item in enumerate(data):
        if not isinstance(item, dict):
            raise ValueError(f"Agendamento no índice {index} não é um objeto.")

        missing_fields = [
            field for field in REQUIRED_APPOINTMENT_FIELDS if field not in item
        ]

        if missing_fields:
            fields = ", ".join(missing_fields)
            raise ValueError(
                f"Agendamento no índice {index} sem campos obrigatórios: {fields}."
            )

    return data
