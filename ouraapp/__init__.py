from flask import Flask
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from ouraapp.database import db
from config import Config

migrate = Migrate()
bootstrap = Bootstrap()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.app_context().push()
    db.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)

    return app


from ouraapp import database
