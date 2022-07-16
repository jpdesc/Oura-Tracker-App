#! /bin/bash

export PATH="/Users/jackdescombes/.venvs/flaskbook/bin:/Users/jackdescombes/opt/anaconda3/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/opt/X11/bin:/Users/jackdescombes/bash_course/scripts"

today=$(date +"%m-%d-%y")

filename="/Users/jackdescombes/db_backups/oura_db_$today.bak"

cd /Users/jackdescombes/projects/oura_proj/ouraapp

pg_dump oura_db > "$filename"

aws s3 sync /Users/jackdescombes/db_backups/ s3://ouradbbackups
