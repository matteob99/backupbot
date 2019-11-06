#!/bin/bash
printenv | sed 's/^\(.*\)$/export \1/g' > /code/env.sh
chmod 0667 /code/env.sh
cron -f
