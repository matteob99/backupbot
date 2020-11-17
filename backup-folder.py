from os import getenv, remove
from datetime import datetime as dt
from botogram.api import TelegramAPI
from botogram import Bot
from subprocess import Popen, PIPE
from glob import glob
bot = Bot(TelegramAPI(api_key=getenv("TG_TOKEN_BACKUP"),
                      endpoint=getenv("TG_ENDPOINT", None)))

date = dt.now().strftime("%Y_%m_%d_%H_%M")
date_file = dt.now().strftime("%Y-%m-%dT%H:%M:%SZ")
split = (f"/usr/bin/zip -r -s {getenv('MAX_SIZE_BACKUP')} " +
         f"date_{getenv('NAME')}.zip /data --password" +
         f" {getenv('BACKUP_PASSWORD')}")
p = Popen(split, shell=True, stdout=PIPE)
p.wait()
chat = bot.chat(getenv("CHAT_BACKUP"))
for i, file in enumerate(glob(f"date_{getenv('NAME')}.z*")):
    text = "#{custom}\n#d{date}\n{file}\nn:{list}".format(
        custom=getenv("NAME"),
        date=date,
        file=f"date_{getenv('NAME')}",
        list=i
        )
    chat.send_file(path=file, caption=text)
for file in glob(f"date_{getenv('NAME')}.z*"):
    remove(file)
print(f"finish backup date_{getenv('NAME')}")
