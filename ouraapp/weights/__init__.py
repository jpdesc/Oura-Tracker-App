from flask import Blueprint

bp = Blueprint('weights', __name__)

from ouraapp.weights import routes
