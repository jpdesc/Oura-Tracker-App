from flask import Blueprint

bp = Blueprint('calendar', __name__)

from ouraapp.calendar import routes
