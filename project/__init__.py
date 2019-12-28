from flask import Flask
from .my_model import db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

def create_app():
    app = Flask(__name__, static_folder = './static')
    app.config.from_object(Config)

    from .app import api_bp
    app.register_blueprint(api_bp)

    db.init_app(app)

    return app

def create_manage():
    app = create_app()
    migrate = Migrate(app, db)
    manager = Manager(app)
    manager.add_command('db', MigrateCommand)
    return manager

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

import os
class Config:
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///app.db"

