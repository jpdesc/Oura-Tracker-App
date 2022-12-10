#! /bin/bash

. /venvs/jenkins_env/bin/activate
cat /srv/jenkins/.env > .env
