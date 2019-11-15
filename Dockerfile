FROM python:3.7-alpine as base
FROM base as builder
COPY requirements.txt /requirements.txt
RUN pip install --install-option="--prefix=/install" -r /requirements.txt

FROM base
COPY --from=builder /install /usr/local
ARG database
RUN apk add  "${database}-client"
RUN mkdir /code
WORKDIR /code
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
COPY backup-cron /etc/cron.d/backup-cron
RUN chmod 0644 /etc/cron.d/backup-cron
RUN crontab /etc/cron.d/backup-cron
COPY start.sh /code/start.sh
RUN chmod 0667  /code/start.sh
COPY "backup-${database}.py" /code/backup.py
CMD ["/code/start.sh"]
