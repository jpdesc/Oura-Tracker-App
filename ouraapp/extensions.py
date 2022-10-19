from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

db = SQLAlchemy(session_options={"autoflush": False})
migrate = Migrate(compare_type=True)
bootstrap = Bootstrap()
login_manager = LoginManager()
mail = Mail()
