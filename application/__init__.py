from flask import Flask

from config import get_config, get_env

from .controller import api
from .ext import db


def configure_app(app):
    app.config.from_object(get_config())
    app.config.from_pyfile(get_env())
    return app


def configure_extensions(app):
    db.init_app(app)
    return app


def create_app():
    app = Flask(__name__)
    configure_app(app)
    configure_extensions(app)
    app.register_blueprint(api)
    return app
