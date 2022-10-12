from flask import Flask
from .extensions import migrate, bootstrap, login_manager, db
from config import Config
from .helpers import update_days_db
import logging
import os


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    with app.app_context():
        db.init_app(app)
        migrate.init_app(app, db)
        bootstrap.init_app(app)
        login_manager.init_app(app)
        login_manager.login_view = 'login'
        from ouraapp.auth import bp as auth_bp
        app.register_blueprint(auth_bp)
        from ouraapp.calendar import bp as cal_bp
        app.register_blueprint(cal_bp)
        from ouraapp.dashboard import bp as dash_bp
        app.register_blueprint(dash_bp, url_prefix='/dashboard')
        from ouraapp.insights import bp as insight_bp
        app.register_blueprint(insight_bp)
        from ouraapp.weights import bp as weights_bp
        app.register_blueprint(weights_bp, url_prefix='/workout')
        from ouraapp.api import bp as api_bp
        app.register_blueprint(api_bp)
        update_days_db()
        if os.getcwd() == '/':
            os.chdir('/srv/jwa')
        logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                            filename=f'{os.getcwd()}/logs/ouraapp.log',
                            level=logging.DEBUG,
                            force=True)
    return app
