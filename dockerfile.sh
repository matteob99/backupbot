#!/usr/bin/sh
if [ "$database" = 'postgresql' ]; then
  echo "apk add postgresql-client"
  apk add postgresql-client
elif [ "$database" = 'mariadb' ]; then
  echo "apk add mariadb-client"
  apk add mariadb-client
elif [ "$database" = "redis" ]; then
  echo "pip install redis"
  pip install redis
elif [ "$database" = "influxdb" ]; then
  echo "apk add influxdb"
  apk  add influxdb
fi
