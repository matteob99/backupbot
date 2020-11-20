import gzip
from sh import pg_dump
from os.path import getmtime
from glob import glob
from subprocess import Popen
from os import getenv, remove
from datetime import datetime as dt
from botogram.api import TelegramAPI
from botogram import Bot
bot = Bot(TelegramAPI(api_key=getenv("TG_TOKEN_BACKUP"),
                      endpoint=getenv("TG_ENDPOINT", None)))
connect = 'postgresql://{username}:{password}@{host}:{port}/{db}'.format(
    username=getenv("POSTGRES_USER"),
    password=getenv("POSTGRES_PASSWORD"),
    host=getenv("POSTGRES_HOST"),
    db=getenv("POSTGRES_DB"),
    port='5432'
)
date = dt.now().strftime("%Y_%m_%d_%H_%M")
file_name = 'backup_{custom}_{date}.gz'.format(custom=getenv("NAME"),
                                               date=date)
with gzip.open(file_name, 'wb') as f:
    print(pg_dump(connect, _out=f))
text = "#{custom}\n#d{date}\n{file}".format(custom=getenv("NAME"),
                                            date=date,
                                            file=file_name)

split = (f"/usr/bin/zip -r -s {getenv('MAX_SIZE_BACKUP')} " +
         f"{file_name}.zip {file_name} --password {getenv('BACKUP_PASSWORD')}")
p = Popen(split, shell=True)
p.wait()

chat = bot.chat(getenv("CHAT_BACKUP"))
for i, file in enumerate(sorted(glob(f"{file_name}.z*"),
                                key=getmtime)):

    text = "#{custom}\n#d{date}\n{file}\nn:{list}".format(
        custom=getenv("NAME"),
        date=date,
        file=file_name,
        list=i
        )
    chat.send_file(path=file, caption=text)
remove(file_name)
for file in glob(f"{file_name}.z*"):
    remove(file)
bot.chat(getenv("CHAT_BACKUP")).send_file(path=file_name,
                                          caption=text)
remove(file_name)
print(f"finish backup {file_name}")
