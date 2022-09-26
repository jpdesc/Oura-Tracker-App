from flask import Blueprint

bp = Blueprint('insights', __name__)

from ouraapp.insights import routes
