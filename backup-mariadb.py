import gzip
from os import getenv, remove
from datetime import datetime as dt
import botogram
from subprocess import Popen, PIPE
bot = botogram.create(getenv("TOKEN_TG"))
date = dt.now().strftime("%Y_%m_%d_%H_%M")
file = 'backup_{custom}_{date}.gz'.format(custom=getenv("NAME"),
                                          date=date)
program = ("/usr/bin/mysqldump --user={user} "+
           "--password={pwd} -h {host} {database}").format(
    user=getenv("MYSQL_USER"),
    pwd=getenv("MYSQL_PASSWORD"),
    host=getenv("MYSQL_HOST"),
    database=getenv("MYSQL_DB"))
print(program)
p = Popen(program, shell=True, stdout=PIPE)
with gzip.open(file, "wb") as f:
    f.writelines(p.stdout)
text = "#{custom}\n#d{date}\n{file}".format(custom=getenv("NAME"),
                                            date=date,
                                            file=file)
bot.chat(getenv("CHAT_BACKUP")).send_file(path=file,
                                          caption=text)
remove(file)
print(f"finish backup {file}")
