import json
import leveldb
from shapely.geometry import Polygon, Point


class AISDatabase:

    def __init__(self):
        self._database_ = leveldb.LevelDB('./database')

    def get_all_entries(self, limit=-1):
        """
        Returns all entries in the database unless limited
        :param limit: the limit of items to return
        :return:
        """
        iterator = self._database_.RangeIter()
        results = {}
        try:
            for entry in iterator:
                results[entry[0].decode()] = entry[1].decode("utf-8")
                if limit > 0:
                    limit -= 1
                    if limit <= 0:
                        break
        finally:
            return results

    def get_entries_in_area(self, point_list):
        """
        Gets all database entries that are geographically located within the provided geometric points list
        :param point_list: the list of points that we are searching within (Note: order of the points is important)
        :return: the list of found database entries that lie within the described geographic polygon
        """
        results = {}
        if len(point_list) < 3:
            return results
        iterator = self._database_.RangeIter()
        area = Polygon(point_list)
        decoder = json.JSONDecoder()
        try:
            for entry in iterator:
                msg = str(entry[1].decode("utf-8"))
                x_pos = AISDatabase.get_value_from_pair(msg, '"x"')["x"]
                y_pos = AISDatabase.get_value_from_pair(msg, '"y"')["y"]
                ship_coord = Point(y_pos, x_pos)
                if area.contains(ship_coord):
                    results[entry[0].decode()] = msg
        finally:
            return results

    def get_entry(self, key):
        """
        Gets a singular entry from the leveldb database with the provided key
        :param key: the key to search for
        :return: The found entry from the database
        """
        return self._database_.Get(bytes(key, "utf-8")).decode("utf-8")

    def search(self, criteria):
        """
        Searches the leveldb database for the provided criteria
        :param criteria: the criteria to search for
        :return: A dictionary of the found matching results
        """
        results = {}
        iterator = self._database_.RangeIter()
        for entry in iterator:
            msg = json.loads(entry[1].decode("utf-8"))
            if ("name" in msg) and (criteria in msg["name"]):
                results[entry[0].decode()] = entry[1].decode("utf-8")
            elif criteria in str(msg["mmsi"]):
                results[entry[0].decode()] = entry[1].decode("utf-8")
        return results

    def search_key(self, key, value):
        """
        Searches the leveldb database checking if the selected key contains the provided value
        :param key: the key to check
        :param value: the value to check for inside the key
        :return: A dictionary of the found matching results
        """
        results = {}
        iterator = self._database_.RangeIter()
        for entry in iterator:
            msg = json.loads(entry[1].decode("utf-8"))
            if key in msg and value in str(msg[key]):
                results[entry[0].decode()] = entry[1].decode("utf-8")
        return results

    @staticmethod
    def get_value_from_pair(target, key):
        decoder = json.JSONDecoder()
        ind = target.index(key)
        comma = target.index(',', ind)
        rslt = target[ind:comma].replace("'", '"')
        return decoder.decode("{{ {0} }}".format(rslt))
