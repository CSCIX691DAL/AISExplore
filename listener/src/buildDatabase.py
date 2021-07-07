import leveldb
import json
import csv
from ais import stream
import argparse
import os

parser = argparse.ArgumentParser(description="Creates a leveldb database after reading the specified file.")
parser.add_argument("-f", "--file", type=str, default="data.csv", help="File containing ais messages to pares")
parser.add_argument("-o", "--output", type=str, default="./", help="destination directory")
parser.add_argument("-d", "--deletedb", nargs='?', type=bool, default=False, help="Deletes the old database.")
args = parser.parse_args()

if args.deletedb:
    leveldb.DestroyDB(os.path.join(args.output, 'database'))
db = leveldb.LevelDB(os.path.join(args.output, 'database'))


def merge_dicts(original, merge):
    return dict(list(merge.items()) + list(original.items()))


def keyExists(key):
    try:
        db.Get(key)
        return True
    except KeyError:
        return False


def encode_str(value):
    return bytes(str(value), "utf-8")


def update_database(msgg):
    parsd = json.loads(msgg)
    if keyExists(encode_str(parsd["mmsi"])):
        old_entry = json.loads(db.Get(encode_str(parsd['mmsi'])).decode("utf-8"))
        new_entry = parsd
        final = merge_dicts(new_entry, old_entry)
        db.Put(encode_str(parsd['mmsi']), str.encode(json.dumps(final)))
    else:
        db.Put(encode_str(parsd['mmsi']), str.encode(json.dumps(parsd)))


with open(args.file) as csvfile:
    for msg in stream.decode(csvfile):
        if msg.get("x", None) is None or msg.get("y", None) is None:
            if keyExists(encode_str(msg["mmsi"])):
                update_database(json.dumps(msg))
            continue
        elif msg['mmsi'] is None:
            print("key missing")
            continue
        update_database(json.dumps(msg))
