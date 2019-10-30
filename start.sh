#!/bin/bash
printenv | sed 's/^\(.*\)$/export \1/g' > /code/env.sh
cron -f