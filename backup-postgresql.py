import gzip
from sh import pg_dump
from os import getenv, remove
from datetime import datetime as dt
import botogram
bot = botogram.create(getenv("TOKEN_TG"))
connect = 'postgresql://{username}:{password}@{host}:{port}/{db}'.format(
    username=getenv("POSTGRES_USER"),
    password=getenv("POSTGRES_PASSWORD"),
    host=getenv("POSTGRES_HOST"),
    db=getenv("POSTGRES_DB"),
    port='5432'
)
date = dt.now().strftime("%Y_%m_%d_%H_%M")
file = 'backup_{custom}_{date}.gz'.format(custom=getenv("NAME"),
                                          date=date)
with gzip.open(file, 'wb') as f:
    print(pg_dump(connect, _out=f))
text = "#{custom}\n#d{date}\n{file}".format(custom=getenv("NAME"),
                                            date=date,
                                            file=file)
bot.chat(getenv("CHAT_BACKUP")).send_file(path=file,
                                          caption=text)
remove(file)
print(f"finish backup {file}")
