import argparse
import os
from datetime import datetime

from ais import stream
from pymongo import MongoClient, errors

from src.functions import more_processing

client = MongoClient('mongodb://useradmin:SOh3TbdfdgPxmt1@bigdata4.research.cs.dal.ca:27011/ais')


# save to mongo
def save_mongo(result):
    try:
        client.ais.ais_data.insert_many(result)

        for message in result:
            more_processing(message)

    except errors.PyMongoError as e:
        print("save_mongo(): ", str(e))


# get time from str to object
def utc_time(date_obj):
    try:
        return datetime.strptime(date_obj, "%Y-%m-%d %H:%M:%S.%f")
    except Exception as e:
        print("utc_time:", str(e))
        return False


# take a file path, read it and parse message,
def read_file_decode(file_path):
    client = MongoClient('mongodb://useradmin:SOh3TbdfdgPxmt1@bigdata4.research.cs.dal.ca:27011/ais')

    lst = []
    print("FileName:", file_path)
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
        print("Finished Decoding", file_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Decode files in a directory')
    parser.add_argument('-dir', help='Directory to Index', type=str)
    parser.add_argument('-file', help='file to parse and decode', )
    args = parser.parse_args()
    if args.dir:
        FileDirectory = args.dir
        files = os.listdir(FileDirectory)
        files = sorted(files)
        for file in files:
            path = FileDirectory + file
            read_file_decode(path)
    elif args.file:
        filename = args.file
        read_file_decode(filename)
