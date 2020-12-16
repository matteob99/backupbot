#!/bin/sh
printenv | sed 's/^\(.*\)$/export \1/g' > /code/env.sh
chmod 0667 /code/env.sh
if [ -n "$CRONTAB_CUSTOM" ]; then
  sed 's/^[^root]*root//g' /etc/cron.d/backup-cron |  xargs echo "$CRONTAB_CUSTOM root" > tempfile
  mv tempfile /etc/cron.d/backup-cron
  crontab /etc/cron.d/backup-cron
fi
/usr/local/bin/python /code/backup.py
crond -f

