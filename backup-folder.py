from os import getenv, remove
from os.path import getmtime
from datetime import datetime as dt
from botogram.api import TelegramAPI
from botogram import Bot
from subprocess import Popen
from glob import glob
from time import sleep
bot = Bot(TelegramAPI(api_key=getenv("TG_TOKEN_BACKUP"),
                      endpoint=getenv("TG_ENDPOINT", None)))

date = dt.now().strftime("%Y_%m_%d_%H_%M")
split = (f"/usr/bin/zip -r -s {getenv('MAX_SIZE_BACKUP','50m')} " +
         f"{date}_{getenv('NAME')}.zip /data --password" +
         f" {getenv('BACKUP_PASSWORD')}")
p = Popen(split, shell=True)
p.wait()
chat = bot.chat(getenv("CHAT_BACKUP"))
for i, file in enumerate(sorted(glob(f"{date}_{getenv('NAME')}.z*"),
                                key=getmtime)):
    text = "#{custom}\n#d{date}\n{file}\nn:{list}".format(
        custom=getenv("NAME"),
        date=date,
        file=f"{date}_{getenv('NAME')}",
        list=i
        )
    chat.send_file(path=file, caption=text)
    sleep(0.13)
for file in glob(f"{date}_{getenv('NAME')}.z*"):
    remove(file)
print(f"finish backup {date}_{getenv('NAME')}")
