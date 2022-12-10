#! /bin/bash

. /venvs/jenkins_env/bin/activate
cat /srv/jenkins/.env > .env
flask db init
flask db migrate
flask db upgrade
