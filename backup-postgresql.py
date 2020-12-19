import gzip
from sh import pg_dump
from os.path import getmtime
from glob import glob
from subprocess import Popen
from os import getenv, remove
from datetime import datetime as dt
from traceback import print_exc
import json
from time import sleep
from requests import get
if getenv("TG_ENDPOINT", None) is None:
    endpoint = "https://api.telegram.org/"
else:
    endpoint = getenv("TG_ENDPOINT")
endpoint += f"bot{getenv('TG_TOKEN_BACKUP')}/"
timeout = int(getenv("TG_TIMEOUT", 10))
chat = getenv("CHAT_BACKUP")
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
try:
    with gzip.open(file_name, 'wb') as f:
        print(pg_dump(connect, _out=f))
    text = "#{custom}\n#d{date}\n{file}".format(custom=getenv("NAME"),
                                                date=date,
                                                file=file_name)

    split = (f"/usr/bin/zip -r -s {getenv('MAX_SIZE_BACKUP')} " +
             f"{file_name}.zip {file_name} --password" +
             f" {getenv('BACKUP_PASSWORD')}")
    p = Popen(split, shell=True)
    p.wait()
    files = []
    content = []
    for i, file in enumerate(sorted(glob(f"{file_name}.z*"),
                                    key=getmtime)):
        content.append({"type": "document",
                        "media": f"attach://document{i}"})
        files.append((f"document{i}", (file, open(file, "rb"))))
        if i % 10 == 0:
            print(content)
            response = get(f"{endpoint}sendMediaGroup",
                           params={'chat_id': chat,
                                   'disable_notification': True,
                                   'media': json.dumps(content)},
                           files=files,
                           timeout=timeout)
            print(response.status_code, response.text)
            content = []
            files = []
        sleep(0.13)
    if len(files) >= 0:
        get(f"{endpoint}sendMediaGroup",
            params={'chat_id': chat,
                    'media': json.dumps(content)},
            files=files,
            timeout=timeout)

    text = "#{custom}\n#d{date}\n{file}".format(
        custom=getenv("NAME"),
        date=date,
        file=f"{date}_{getenv('NAME')}",
    )
    get(f"{endpoint}sendMessage",
        params={'chat_id': chat,
                'text': text,
                'parse_mode': 'HTML'})

except Exception:
    print_exc()
remove(file_name)
for file in glob(f"{file_name}.z*"):
    remove(file)

remove(file_name)
print(f"finish backup {file_name}")
