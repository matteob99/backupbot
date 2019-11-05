FROM python:3.7-alpine as base
FROM base as builder
COPY requirements.txt /requirements.txt
RUN pip install --install-option="--prefix=/install" -r /requirements.txt

FROM base
COPY --from=builder /install /usr/local
RUN mkdir /code
WORKDIR /code
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN touch /code/env.sh; chmod 0667 /code/env.sh
COPY backup-cron /etc/cron.d/backup-cron
RUN chmod 0644 /etc/cron.d/backup-cron
RUN crontab /etc/cron.d/backup-cron
COPY backup.py /code/backup.py
COPY start.sh /code/start.sh
RUN chmod 0667  /code/start.sh
CMD ["/code/start.sh"]
