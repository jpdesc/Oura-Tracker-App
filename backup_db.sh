#! /bin/bash

export PATH="/Users/jackdescombes/.venvs/flaskbook/bin:/Users/jackdescombes/opt/anaconda3/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/opt/X11/bin:/Users/jackdescombes/bash_course/scripts"

max_files=5
today=$(date +"%m-%d-%y")

filename="/Users/jackdescombes/db_backups/oura_db_$today.bak"

cd /Users/jackdescombes/projects/oura_proj/ouraapp

pg_dump oura_db > "$filename"

cd /Users/jackdescombes/db_backups/

aws s3 sync /Users/jackdescombes/db_backups/ s3://ouradbbackups

file_count=$(aws s3 ls --recursive s3://ouradbbackups | wc -l)
excess=$(($file_count-$max_files))
echo $file_count

if [ $file_count -gt $max_files ]
then
ls -t | tail -$excess | xargs rm
aws s3 sync . s3://ouradbbackups --delete
fi
