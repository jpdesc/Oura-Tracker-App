#!/usr/bin/python3.9

import logging
import sys

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/srv/jwa/ouraapp')
from ouraapp import app as application
