from flask import Blueprint, jsonify


api = Blueprint("api", __name__, url_prefix="/api")


@api.get("/appointments")
def appointments():
    data = [
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
        },
        {
            "id": 2,
            "patient": "Bruno Almeida",
            "cpf": "234.567.890-11",
            "doctor": "Dra. Marina Lopes",
            "specialty": "Dermatologia",
            "date": "2026-07-22",
            "time": "10:30",
            "insurance": "Bradesco Saúde",
            "status": "Pendente",
        },
        {
            "id": 3,
            "patient": "Carla Ribeiro",
            "cpf": "345.678.901-22",
            "doctor": "Dr. Felipe Rocha",
            "specialty": "Ortopedia",
            "date": "2026-07-23",
            "time": "14:00",
            "insurance": "SulAmérica",
            "status": "Confirmado",
        },
        {
            "id": 4,
            "patient": "Daniel Martins",
            "cpf": "456.789.012-33",
            "doctor": "Dra. Helena Costa",
            "specialty": "Pediatria",
            "date": "2026-07-24",
            "time": "08:30",
            "insurance": "Amil",
            "status": "Cancelado",
        },
        {
            "id": 5,
            "patient": "Eduarda Lima",
            "cpf": "567.890.123-44",
            "doctor": "Dr. Renato Alves",
            "specialty": "Neurologia",
            "date": "2026-07-24",
            "time": "16:00",
            "insurance": "Particular",
            "status": "Confirmado",
        },
        {
            "id": 6,
            "patient": "Fernando Gomes",
            "cpf": "678.901.234-55",
            "doctor": "Dra. Paula Fernandes",
            "specialty": "Endocrinologia",
            "date": "2026-07-25",
            "time": "11:15",
            "insurance": "NotreDame Intermédica",
            "status": "Reagendado",
        },
    ]

    return jsonify(data)
