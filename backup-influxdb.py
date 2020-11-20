from os import getenv, remove
from os.path import isfile
from datetime import datetime as dt
from botogram.api import TelegramAPI
from botogram import Bot
from subprocess import Popen, PIPE
from os.path import getmtime
from glob import glob
from time import sleep
bot = Bot(TelegramAPI(api_key=getenv("TG_TOKEN_BACKUP"),
                      endpoint=getenv("TG_ENDPOINT", None)))

date = dt.now().strftime("%Y_%m_%d_%H_%M")
file_name = 'backup_{custom}_{date}'.format(custom=getenv("NAME"),
                                            date=date)
if isfile("/data/last_start"):
    with open("/data/last_start", 'r') as file:
        start = f"-start {file.read()}"
else:
    start = ""
date_file = dt.now().strftime("%Y-%m-%dT%H:%M:%SZ")
program = ("influxd backup -host {host}:{port}  -portable {path} {start}"
           ).format(host=getenv("INFLUXDB_HOST"),
                    port=getenv("INFLUXDB_PORT"),
                    path=file_name,
                    start=start)
p = Popen(program, shell=True, stdout=PIPE)
p.wait()
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
    sleep(0.13)
remove(file_name)
for file in glob(f"{file_name}.z*"):
    remove(file)
with open('/data/last_start', 'w') as file:
    file.write(date_file)
print(f"finish backup {file_name}")
