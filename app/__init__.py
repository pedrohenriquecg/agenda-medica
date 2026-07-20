from flask import Flask

from app.config import Config
from app.mock_api import api
from app.routes import main


def create_app() -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    app.register_blueprint(main)
    app.register_blueprint(api)

    return app
