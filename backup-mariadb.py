import gzip
from os import getenv, remove
from datetime import datetime as dt
from botogram.api import TelegramAPI
from botogram import Bot
from subprocess import Popen, PIPE
from os.path import getmtime
from glob import glob
bot = Bot(TelegramAPI(api_key=getenv("TG_TOKEN_BACKUP"),
                      endpoint=getenv("TG_ENDPOINT", None)))

date = dt.now().strftime("%Y_%m_%d_%H_%M")
file_name = 'backup_{custom}_{date}.gz'.format(custom=getenv("NAME"),
                                               date=date)
database = getenv("MYSQL_DB", None)
if database is None or database.lower() == 'all':
    database = "--all-databases"
program = ("/usr/bin/mysqldump --user={user} " +
           "--password={pwd} -h {host} {database}").format(
    user=getenv("MYSQL_USER"),
    pwd=getenv("MYSQL_PASSWORD"),
    host=getenv("MYSQL_HOST"),
    database=database)
p = Popen(program, shell=True, stdout=PIPE)
with gzip.open(file_name, "wb") as f:
    f.writelines(p.stdout)
split = (f"/usr/bin/zip -r -s {getenv('MAX_SIZE_BACKUP')} " +
         f"{file_name}.zip {file_name} --password {getenv('BACKUP_PASSWORD')}")
p = Popen(split, shell=True)
p.wait()
chat = bot.chat(getenv("CHAT_BACKUP"))
for i, file in enumerate(sorted(glob(f"{file_name}.z*"), key=getmtime)):
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
print(f"finish backup {file_name}")
