import requests


def fetch_appointments(api_url: str, timeout: int) -> list[dict]:
    response = requests.get(api_url, timeout=timeout)
    response.raise_for_status()

    data = response.json()

    if not isinstance(data, list):
        raise ValueError("A API retornou um formato de dados inválido.")

    return data
