from flask import Flask

from futdata.ext import config


def create_app(import_name='futdata'):
    app = Flask(import_name)
    config.init_app(app)
    return app
