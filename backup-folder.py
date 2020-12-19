from os import getenv, remove
from os.path import getmtime
from datetime import datetime as dt
from traceback import print_exc
from subprocess import Popen
from glob import glob
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

try:
    date = dt.now().strftime("%Y_%m_%d_%H_%M")
    split = (f"/usr/bin/zip -r -s {getenv('MAX_SIZE_BACKUP','50m')} " +
             f"{date}_{getenv('NAME')}.zip /data --password" +
             f" {getenv('BACKUP_PASSWORD')}")
    p = Popen(split, shell=True)
    p.wait()
    files = []
    content = []
    for i, file in enumerate(sorted(glob(f"{date}_{getenv('NAME')}.z*"),
                                    key=getmtime), start=1):
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
for file in glob(f"{date}_{getenv('NAME')}.z*"):
    remove(file)
print(f"finish backup {date}_{getenv('NAME')}")
