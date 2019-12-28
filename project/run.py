from flask import Flask
from my_model import db


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from app import api_bp
    app.register_blueprint(api_bp)

    db.init_app(app)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

import os
class Config:
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///app.db"

