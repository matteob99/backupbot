FROM python:3.7-alpine as base

FROM base as builder
COPY requirements.txt /requirements.txt
RUN pip install --prefix=/install -r /requirements.txt --no-warn-script-location

FROM base
COPY --from=builder /install /usr/local
ARG database
ENV DATABASENAME $database
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apk add zip
COPY dockerfile.sh /dockerfile.sh
RUN chmod 777 /dockerfile.sh
RUN sh /dockerfile.sh
RUN rm /dockerfile.sh
RUN mkdir /code
WORKDIR /code
COPY backup-cron /etc/cron.d/backup-cron
RUN chmod 0644 /etc/cron.d/backup-cron
RUN crontab /etc/cron.d/backup-cron
COPY start.sh /code/start.sh
RUN chmod 0667  /code/start.sh
VOLUME /data
COPY "backup-${database}.py" /code/backup.py
CMD ["/code/start.sh"]
