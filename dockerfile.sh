#!/usr/bin/sh
if [ "$database" = 'postgresql' ]; then
  apk add postgresql-client
elif [ "$database" = 'mariadb' ]; then
  apk add mariadb-client
elif [ "$database" = "redis" ]; then
  pip install redis
elif [ "$database" = "influxdb" ]; then
  apk  add influxdb
fi
