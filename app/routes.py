from flask import Blueprint


main = Blueprint("main", __name__)


@main.get("/")
def index() -> str:
    return "Agenda Médica funcionando!"
