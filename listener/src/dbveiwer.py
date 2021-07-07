import leveldb

db = leveldb.LevelDB('./database')

x = db.RangeIter()
for entry in x:
    print("MMSI: " + entry[0].decode(), "Info: " + str(eval(entry[1].decode("utf-8"))))