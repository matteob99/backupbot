#!/bin/sh
printenv | sed 's/^\(.*\)$/export \1/g' > /code/env.sh
chmod 0667 /code/env.sh
crond -f

