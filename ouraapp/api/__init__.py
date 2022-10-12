from flask import Blueprint

bp = Blueprint('api', __name__)

from ouraapp.api import routes
