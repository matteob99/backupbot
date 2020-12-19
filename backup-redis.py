import redis
from time import time, sleep
from os.path import getmtime
import os
from os import getenv
from traceback import print_exc
from subprocess import Popen
from glob import glob
import json
from requests import get


def dumpredis(redisdb):
    r = redis.StrictRedis(host=redisdb["host"], port=redisdb["port"],
                          db=redisdb["db"], password=redisdb["password"])
    a = {"name": redisdb["name"]}
    b = {}
    for key in r.keys("*"):
        try:
            c = r.hgetall(key.decode("utf-8"))
            d = {}
            for e in c:
                try:
                    d[e.decode('utf-8')] = int(c[e])
                except Exception:
                    if c[e] == b"True":
                        d[e.decode('utf-8')] = True
                    elif c[e] == b"False":
                        d[e.decode('utf-8')] = False
                    else:
                        d[e.decode('utf-8')] = c[e].decode('utf-8')
            b.update({key.decode("utf-8"): d})
        except Exception:
            pass

    a.update({"value": b})
    return a


def dumpredisall(redisdball=None, path=None):
    if not path:
        path = './redisdump' + str(int(time())) + '.json'
    redisjsonall = []
    for redisdb in redisdball:
        redisjsonall.append(dumpredis(redisdb))
    with open(path, 'w') as jsonfile:
        json.dump(redisjsonall, jsonfile, indent=4, sort_keys=True)
    return path


def alldb(host="localhost", port=6379, password=None, name="redisdb",
          idb=0, fdb=10, redisdball=[]):
    for i in range(idb, fdb + 1):
        redisdball.append({"host": host, "port": port,
                           "db": i, "password": password,
                           "name": str(name) + 'db' + str(i)})

    return redisdball


def restoredb(host="localhost", port=6379, password=None, db=0,
              name="redisdb", path=None):
    if not path:
        return False
    r = redis.StrictRedis(host=host, port=port,
                          db=db, password=password)
    with open(path, 'r') as jsonfile:
        a = json.load(jsonfile)
        print(name)
        for b in a:
            if b["name"] == name:
                print(b["name"],
                      b["name"] == name)
                jsondb = b
                break
    for a in jsondb["value"]:
        for b in jsondb["value"][a]:
            #    print(a, b, jsondb["value"][a][b])
            r.hset(a, b, str(jsondb["value"][a][b]))

    return True


def cryptoandcompresspath(path, pathdest=None):
    if pathdest is None:
        pathdest = path+'.zip'
    split = (f"/usr/bin/zip -r -s {getenv('MAX_SIZE_BACKUP')} " +
             f"{pathdest} {path} --password {getenv('BACKUP_PASSWORD')}")
    p = Popen(split, shell=True)
    p.wait()
    return pathdest


def main():
    t = time()
    if getenv("TG_ENDPOINT", None) is None:
        endpoint = "https://api.telegram.org/"
    else:
        endpoint = getenv("TG_ENDPOINT")
    endpoint += f"bot{getenv('TG_TOKEN_BACKUP')}/"
    timeout = int(getenv("TG_TIMEOUT", 10))
    chat = getenv("CHAT_BACKUP")
    redisdball = []
    listdb = ""
    redisdball = alldb(host=getenv("REDIS_HOST"),
                       port=int(getenv("REDIS_PORT")),
                       password=getenv("REDIS_PASSWORD"),
                       name=getenv("NAME"),
                       redisdball=redisdball)
    listdb += "\n#{name}".format(name=getenv("NAME"))
    path1 = dumpredisall(redisdball)
    path = cryptoandcompresspath(path1)
    os.remove(path1)

    try:
        files = []
        content = []
        for i, file in enumerate(sorted(
                glob(f"{'.'.join(path.split('.')[:-1])}.*"),
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
        text = "#{path}\ntime:{time}s\nlistdb:{listdb}".format(
            path=path[2:-9],
            time=time() - t,
            listdb=listdb)
        get(f"{endpoint}sendMessage",
            params={'chat_id': chat,
                    'text': text,
                    'parse_mode': 'HTML'})

        sleep(0.13)
    except Exception:
        print_exc()
    os.remove(path)
    for file in glob(f"{'.'.join(path.split('.')[:-1])}.*"):
        os.remove(file)


if __name__ == "__main__":
    main()
