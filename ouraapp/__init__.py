from flask import Flask
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from ouraapp.database import db
from config import Config
from ouraapp.fetch_oura_data import setup_oura_data

migrate = Migrate()
bootstrap = Bootstrap()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    # app.app_context().push()
    with app.app_context():
        db.init_app(app)
        migrate.init_app(app, db)
        bootstrap.init_app(app)
        setup_oura_data()
    return app


from ouraapp import database
