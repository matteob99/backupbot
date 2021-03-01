from os import getenv, remove, removedirs
from os.path import isfile, isdir
from datetime import datetime as dt
from subprocess import Popen, PIPE
from os.path import getmtime
from glob import glob
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
try:
    p = Popen(program, shell=True, stdout=PIPE)
    p.wait()
    split = (f"/usr/bin/zip -r -s {getenv('MAX_SIZE_BACKUP')} " +
             f"{file_name}.zip {file_name} " +
             f"--password {getenv('BACKUP_PASSWORD')}")
    p = Popen(split, shell=True)
    p.wait()
    files = []
    content = []
    for i, file in enumerate(sorted(glob(f"{file_name}.z*"),
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
        response = get(f"{endpoint}sendMediaGroup",
                       params={'chat_id': chat,
                               'media': json.dumps(content)},
                       files=files,
                       timeout=timeout)
        print(response.status_code, response.text)

    text = "#{custom}\n#d{date}\n{file}".format(
        custom=getenv("NAME"),
        date=date,
        file=f"{date}_{getenv('NAME')}",
    )
    response = get(f"{endpoint}sendMessage",
                   params={'chat_id': chat,
                           'text': text,
                           'parse_mode': 'HTML'})
    print(response.status_code, response.text)

except Exception:
    print_exc()
if isfile(file_name):
    remove(file_name)
elif isdir(file_name):
    for file in glob(f"{file_name}/*"):
        remove(file)
    removedirs(file_name)
for file in glob(f"{file_name}.z*"):
    remove(file)
with open('/data/last_start', 'w') as file:
    file.write(date_file)
print(f"finish backup {file_name}")
