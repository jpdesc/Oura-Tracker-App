from flask import Flask
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from ouraapp.database import db
from config import Config
from flask_login import LoginManager
from ouraapp.fetch_oura_data import update_days_db
import logging
from imp import reload

migrate = Migrate(compare_type=True)
bootstrap = Bootstrap()
login_manager = LoginManager()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    with app.app_context():
        db.init_app(app)
        migrate.init_app(app, db)
        bootstrap.init_app(app)
        login_manager.init_app(app)
        login_manager.login_view = 'login'
        update_days_db()
        reload(logging)
        logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                            filename='/srv/jwa/logs/ouraapp.log',
                            level=logging.DEBUG)
        logger = logging.getLogger("ouraapp")
    return app


from ouraapp import database
