from flask import Blueprint

bp = Blueprint('dashboard', __name__)

from ouraapp.dashboard import routes
