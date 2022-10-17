from flask import Blueprint

bp = Blueprint('profile', __name__)

from ouraapp.profile import routes
