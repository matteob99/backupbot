# backupbot

ita 🇮🇹

backupbot e' un insieme di imagini docker per creare backup schedulati di diversi database

backup supportati:
- [influxdb](ghcr.io/matteob99/backupbot:influxdb-latest)
- [mariadb](ghcr.io/matteob99/backupbot:mariadb-latest)
- [postgresql](ghcr.io/matteob99/backupbot:postgresql-latest)
- [redis](ghcr.io/matteob99/backupbot:redis-latest)
- [folder](ghcr.io/matteob99/backupbot:folder-latest)

###env comuni:
- TG_TOKEN_BACKUP: token del bot
- TG_ENDPOINT: endpoint delle bot api di default https://api.telegram.org/
- NAME: nome del backup
- MAX_SIZE_BACKUP: larghezza massima del file (se si usa un endpoint standard e' 9M)
- BACKUP_PASSWORD: password del zip di backup
- CHAT_BACKUP: chat dove mandare i file
- CRONTAB_CUSTOM: di default e' ogni giorno a mezzanotte se si vuole cambiare seguire la doc di [crontab](https://man7.org/linux/man-pages/man5/crontab.5.html)

###env influxdb:
- INFLUXDB_HOST: indirizzo del server influxdb
- INFLUXDB_PORT: porta del server influxdb

###env mariadb
- MYSQL_USER: utente di mariadb
- MYSQL_PASSWORD: password dell'utente mariadb
- MYSQL_HOST: indirizzo del server mariadb
- MYSQL_DB: database backup se non indicato o è ``all`` sono tutti quanti i database

###env postgresql
- POSTGRES_USER: utente di postgresql
- POSTGRES_PASSWORD: password dell'utente postgresql
- POSTGRES_HOST: indirizzo del server postgresql
- POSTGRES_DB: database backup

###env redis 
- REDIS_PASSWORD: password del database redis
- REDIS_HOST: indirizzo del server redis
- REDIS_PORT: porta del server redis
- REDIS_DB: database backup


esempio per mariadb

```bash
docker run -d --env TG_TOKEN_BACKUP=token_bot --env NAME=mariadb --env MAX_SIZE_BACKUP=9M \
              --env BACKUP_PASSWORD=password_backup --env CHAT_BACKUP=123456789\
              --env MYSQL_USER=root --env MYSQL_PASSWORD=PASSWORD --env MYSQL_HOST=mariadb --env MYSQL_DB=all \
              docker pull ghcr.io/matteob99/backupbot:mariadb-latest
```

esempio per una cartella
```bash
docker run -d --env TG_TOKEN_BACKUP=token_bot --env NAME=mariadb --env MAX_SIZE_BACKUP=9M \
              --env BACKUP_PASSWORD=password_backup --env CHAT_BACKUP=123456789\
              -v folder_path:/data
              docker pull ghcr.io/matteob99/backupbot:folder-latest
```