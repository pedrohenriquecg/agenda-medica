from flask import Blueprint, redirect, render_template, request, session, url_for

from app.auth import validate_user


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

        if validate_user(username, password):
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

    return render_template("agenda.html", username=username)


@main.get("/logout")
def logout():
    session.clear()
    return redirect(url_for("main.login"))
