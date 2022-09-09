#! /bin/bash

export PATH="/jwa_env/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/srv/jwa/ouraapp"

max_files=5
today=$(date +"%m-%d-%y")

filename="/var/lib/ouraapp/backups/uploads/oura_db_$today.bak"

cd /srv/jwa

su postgres

pg_dump oura_db > "$filename"

cd /var/lib/ouraapp/backups/uploads/

chmod 777 *

aws s3 sync /var/lib/ouraapp/backups/uploads/ s3://ouradbbackups

file_count=$(aws s3 ls --recursive s3://ouradbbackups | wc -l)
excess=$(($file_count-$max_files))
echo $file_count

if [ $file_count -gt $max_files ]
then
ls -t | tail -$excess | xargs rm
aws s3 sync . s3://ouradbbackups --delete
fi

rsync -avp root@server.jpdesc.com:/var/lib/ouraapp/backups/uploads/* /Users/jackdescombes/db_backups/
