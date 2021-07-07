import logging
import platform
from datetime import datetime
from multiprocessing import Process, Pool
from time import sleep

import psutil
from ais import stream
from pymongo import MongoClient, errors
from requests import post

from src.functions import more_processing

software_version = 0.2
inFile = "ais_undecoded.msg"
outFile = 'ais_decoded.txt'
LOG_FILE_NAME = "decoder.log"
HCTK_URL = 'http://bigdata2.research.cs.dal.ca:8087/beat'


def save_mongo(result):
    client = MongoClient('mongodb://useradmin:SOh3TbdfdgPxmt1@bigdata4.research.cs.dal.ca:27011/ais')
    try:
        client.ais.ais_data.insert_many(result)
        for message in result:
            more_processing(message)
    except errors.PyMongoError as e:
        print("save_mongo(): ", str(e))


def utc_time(date_obj):
    try:
        return datetime.strptime(date_obj, "%Y-%m-%d %H:%M:%S.%f")
    except Exception as e:
        print("utc_time():", str(e))


# take a file path, read it and parse message,
def read_file_decode(file_path):
    client = MongoClient('mongodb://useradmin:SOh3TbdfdgPxmt1@bigdata4.research.cs.dal.ca:27011/ais')
    lst = []

    logging.error("Starting on file: " + file_path)
    counter = 0
    with open(file_path) as msg_file:
        for msg in stream.decode(msg_file):
            msg['batch'] = True
            time = utc_time(msg_file.readline().strip('\n'))
            if time:
                msg['event_time'] = time
                try:
                    x = msg.get('x', None)
                    y = msg.get('y', None)
                    if x is not None and y is not None and abs(x) <= 180 and abs(y) < 90:
                        msg['location'] = {'type': 'Point', 'coordinates': [x, y]}
                except Exception as e:
                    print("read_file_decode():", str(e))

                if len(lst) != 1000:
                    lst.append(msg)
                else:
                    save_mongo(lst)
                    lst.clear()
                    lst.append(msg)
        if lst:
            save_mongo(lst)
            lst.clear()
        logging.error("Finished Decoding " + file_path)
        with open(outFile, 'a+') as outF:
            outF.write(file_path + '\n')


def system_status():
    os, name, version, _, _, _ = platform.uname()
    version = version.split('-')[0]
    cores = psutil.cpu_count()
    cpu_percent = psutil.cpu_percent()
    memory_percent = psutil.virtual_memory()[2]
    disk_percent = psutil.disk_usage('/')[3]
    boot_time = datetime.fromtimestamp(psutil.boot_time())
    running_since = boot_time.strftime("%A %d. %B %Y")
    res = {
        "os": os,
        "OS Version": version,
        "health_check_repeat": 600,
        "name": "File Decoder",
        "cores": cores,
        'risk_mitigation_file': __file__,
        "disk percent": disk_percent,
        "cpu percent": cpu_percent,
        "memory percent": memory_percent,
        "running since": running_since,
        "App version": software_version
    }
    return res


def health_check():
    while 1:
        print("Calling Health Check")
        try:
            res = system_status()
            upload(res)
        except Exception as e:
            print("health_check():" + str(e))
        finally:
            sleep(600)


def upload(data):
    try:
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        post(HCTK_URL, json=data, headers=headers, timeout=40)
    except Exception as e:
        print("hchk:" + e)


def follow(thefile):
    thefile.seek(0, 2)
    while True:
        line = thefile.readline()
        if not line:
            sleep(0.1)
            continue
        yield line


def decode_pool(values):
    pool = Pool(processes=10)
    pool.map(read_file_decode, values)


def decode_proc():
    inputFile = open(inFile, 'r')
    inputFiles = [x.rstrip() for x in inputFile]
    Process(target=decode_pool, args=(inputFiles,)).start()
    input_lines = follow(inputFile)
    for line in input_lines:
        print("Working on:", line)
        line = line.rstrip()
        Process(target=read_file_decode(line)).start()


if __name__ == '__main__':
    for handler in logging.root.handlers[:]: logging.root.removeHandler(handler)

    logging.basicConfig(level=logging.ERROR, format='%(asctime)s:\n %(message)s\n',
                        datefmt='%m/%d/%Y %I:%M:%S %p', filename=LOG_FILE_NAME)

    logging.error("Running at " + str(datetime.now()))

    try:
        Process(target=decode_proc).start()
        Process(target=health_check, daemon=True).start()
    except Exception as e:
        print("main():" + str(e))
