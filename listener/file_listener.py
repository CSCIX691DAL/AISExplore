import logging
import os
import platform
import socket
from datetime import datetime
from multiprocessing import Process
from threading import Thread
from time import sleep

import psutil
import requests as req

HOST = 'data.aishub.net'
HCTK_URL = 'http://bigdata2.research.cs.dal.ca:8087/beat'
PORT = 4053
counter = 0
software_version = 0.21
TIME_INTERVAL = 600
SHORT_TIME_INTERVAL = 20
VERY_SHORT_TIME_INTERVAL = 5
LOG_FILE_NAME = 'file_listener.log'
DONE_FILES = 'ais_undecoded.msg'
STORAGE_PATH = os.getcwd() + '/'

print('connecting to {} port {}'.format(HOST, PORT))


def countdown(resp, t=TIME_INTERVAL):
    while t:
        mins, secs = divmod(t, 60)
        time_format = '{:02d}:{:02d}'.format(mins, secs)
        print(time_format, end='\r')
        sleep(1)
        t -= 1
    resp['value'] = True
    return resp


# socket listener, generator style to receive data
# and save it to file
def readlines(sock_h, recv_buffer=1024, delim='\n'):
    buf = ''
    data = True
    while data:
        data = sock_h.recv(recv_buffer)
        buf += data.decode('utf-8')
        while buf.find(delim) != -1:
            line, buf = buf.split('\n', 1)
            yield line


def network_to_file(file_name, response):
    save_to_logfile("Writing to " + file_name)
    with open(file_name, 'w+') as file:
        while not response['value']:
            for data in readlines(sock):
                file.write(data + '\n' + str(datetime.utcnow()) + '\n')
                if response['value']:
                    break
            file.close()


def net_file_app():
    response = {'value': False}
    Thread(target=countdown, args=(response,)).start()

    file_name = str(datetime.now())[:-10] + '.csv'

    fpath = STORAGE_PATH + file_name[:10].replace('-', '/') + '/'

    if not os.path.exists(fpath):
        print('Created Directory', fpath)
        os.makedirs(fpath)
    file_name = fpath + file_name
    network_to_file(file_name, response)

    with open(DONE_FILES, 'a+') as f_decode:
        f_decode.write(file_name + '\n')


def f_loop():
    save_to_logfile("Starting f_loop()" + str(datetime.now()))
    while True:
        try:
            net_file_app()
        except Exception as ex:
            save_to_logfile(str(ex))


def system_status():
    os, name, version, _, _, _ = platform.uname()
    version = version.split('-')[0]
    cores = psutil.cpu_count()
    cpu_percent = psutil.cpu_percent()
    memory_percent = psutil.virtual_memory()[2]
    disk_percent = psutil.disk_usage('/')[3]
    boot_time = datetime.fromtimestamp(psutil.boot_time())
    running_since = boot_time.strftime("%A %d. %B %Y")
    desc = "This service is running on {} and recieves data from AISHUB on {} port {} and saves them to path {}".format(
        name, HOST, PORT, STORAGE_PATH)
    res = {"os": os,
           "OS Version": version,
           "name": "File Listener on {}".format(name),
           "cores": cores,
           "disk percent": disk_percent,
           "cpu percent": cpu_percent,
           "memory percent": memory_percent,
           "running since": running_since,
           "description": desc,
           "health_check_repeat": TIME_INTERVAL,
           "App version": software_version}
    return res


def save_to_logfile(msg):
    logging.error(msg)


def health_check():
    sleep(SHORT_TIME_INTERVAL)
    save_to_logfile('Health Check started')
    while True:
        try:
            res = system_status()
            upload(res)
        except Exception as e:
            save_to_logfile("health_check():" + str(e))
        finally:
            sleep(TIME_INTERVAL)


def upload(data):
    try:
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        _ = req.post(HCTK_URL, json=data, headers=headers, timeout=3.5)
    except Exception as e:
        save_to_logfile("hchk():" + str(e))


if __name__ == '__main__':
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    logging.basicConfig(level=logging.ERROR,
                        format='%(asctime)s:\n %(message)s\n',
                        datefmt='%m/%d/%Y %I:%M:%S %p',
                        filename=LOG_FILE_NAME)
    logging.error("Started Logging at " + str(datetime.now().time()))

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect((HOST, PORT))
        Process(target=f_loop).start()
        Process(target=health_check).start()
    except Exception as e:
        save_to_logfile("main():" + str(e))
