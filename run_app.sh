#!/bin/bash

cd /srv/jwa/ouraapp


. /jwa_env/bin/activate


python3.9 app.py >> ./logs/run_err.log
