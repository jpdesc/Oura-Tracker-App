import os
import logging
from flask import Flask
from .extensions import migrate, bootstrap, login_manager, db, mail
from .helpers import update_days_db
# import flask_monitoringdashboard as dashboard_monitor


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('../config.py')
    print(f'current directory contents: {os.listdir()}')
    # dashboard_monitor.config.init_from(file='config.cfg')

    with app.app_context():
        db.init_app(app)
        migrate.init_app(app, db)
        bootstrap.init_app(app)
        mail.init_app(app)
        login_manager.init_app(app)
        login_manager.login_view = 'login'
        # dashboard_monitor.bind(app)
        update_days_db()
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
        from ouraapp.profile import bp as profile_bp
        app.register_blueprint(profile_bp)

        if os.getcwd() == '/':
            os.chdir('/srv/jwa')
        logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                            filename=f'{os.getcwd()}/logs/ouraapp.log',
                            level=logging.DEBUG,
                            force=True)
    return app
