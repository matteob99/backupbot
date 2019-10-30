FROM python:3.7-slim
RUN mkdir /code
WORKDIR /code
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apt-get update && apt-get -y install cron postgresql-client
COPY requirements.txt /code/requirements.txt
RUN touch /code/env.sh; chmod 0667 /code/env.sh
RUN pip install --no-cache-dir -r requirements.txt
COPY backup-cron /etc/cron.d/backup-cron
RUN chmod 0644 /etc/cron.d/backup-cron
RUN crontab /etc/cron.d/backup-cron
COPY backup.py /code/backup.py
COPY start.sh /code/start.sh
RUN chmod 0667  /code/start.sh
CMD ["/code/start.sh"]
