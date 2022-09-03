#!/usr/bin/python3

import logging
import sys

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/srv/jwa/oura_proj')
import run as application
