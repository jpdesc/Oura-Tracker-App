from flask import Blueprint

bp = Blueprint('auth', __name__)

from ouraapp.auth import routes
