from requests import RequestException

from flask import Blueprint, current_app, redirect, render_template, request, session, url_for

from app.auth import AuthenticationDatabaseError, validate_user
from app.services.appointment_api import fetch_appointments


main = Blueprint("main", __name__)


@main.get("/")
def index():
    return redirect(url_for("main.login"))


@main.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        try:
            user_is_valid = validate_user(username, password)
        except AuthenticationDatabaseError:
            current_app.logger.exception("Erro ao acessar o banco de dados durante login.")
            error = "Não foi possível acessar o sistema no momento. Tente novamente mais tarde."
            return render_template("login.html", error=error)

        if user_is_valid:
            session.clear()
            session["username"] = username
            return redirect(url_for("main.agenda"))

        error = "Usuário ou senha inválidos."

    return render_template("login.html", error=error)


@main.get("/agenda")
def agenda():
    username = session.get("username")

    if username is None:
        return redirect(url_for("main.login"))

    appointments = []
    appointments_error = None

    try:
        appointments = fetch_appointments(
            current_app.config["APPOINTMENTS_API_URL"],
            current_app.config["APPOINTMENTS_API_TIMEOUT"],
        )
    except (RequestException, ValueError):
        current_app.logger.exception("Erro ao carregar agendamentos.")
        appointments_error = "Não foi possível carregar os agendamentos."

    return render_template(
        "agenda.html",
        username=username,
        appointments=appointments,
        appointments_error=appointments_error,
    )


@main.get("/logout")
def logout():
    session.clear()
    return redirect(url_for("main.login"))
