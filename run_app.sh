#!/bin/bash

cd /srv/jwa/ouraapp

mkdir logs

. /jwa_env/bin/activate


python3.9 app.py >> ./logs/run_err.log
