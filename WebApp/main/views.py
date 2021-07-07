import json
import socket
from json import JSONDecodeError
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
import threading

from util import AISDatabase

database = AISDatabase.AISDatabase()

from RealTimeAIS.db_connection import get_postgres


def send_ais_ship_message(messages):
    for key in messages:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(("localhost", 1337))
        message = json.loads(messages[key])  # dictionary of AIS message
        mmsi = message["mmsi"]  # lat is y
        lat = message["y"]  # lat is y
        lon = message["x"]  # long is x
        cog = message.get("cog", 0)  # rotation default to zero
        msg = '{' + '"mmsi": {}, "lat": {}, "lon": {}, "cog": {}'.format(mmsi, lat, lon, cog) + '}'
        sock.sendall(msg.encode())
        sock.close()


def index(request):
    return render(request, 'index.html')


def latest(request):
    results = database.get_all_entries()
    thread = threading.Thread(target=send_ais_ship_message, args=(results,))
    thread.daemon = True
    thread.start()
    return JsonResponse({'results': "Results Returned"})


def raw_latest(request):
    results = database.get_all_entries()
    return JsonResponse({'results': results})


def region(request, points):
    try:
        points_dict = json.loads(points)
    except JSONDecodeError:
        return JsonResponse({'results': 'Invalid Input - Not valid json.'})

    point_list = []
    for entry in points_dict:
        val = points_dict[entry]
        if (type(val) is not list) or len(val) < 2 < len(val):
            return JsonResponse({'results': 'Invalid Input - Input not a valid coordinate point.'})
        else:
            point_list.append(val)

    results = database.get_entries_in_area(point_list)
    thread = threading.Thread(target=send_ais_ship_message, args=(results,))
    thread.daemon = True
    thread.start()
    return JsonResponse({'results': "Results Returned"})


def raw_region(request, points):
    try:
        points_dict = json.loads(points)
    except JSONDecodeError:
        return JsonResponse({'results': 'Invalid Input - Not valid json.'})

    point_list = []
    for entry in points_dict:
        val = points_dict[entry]
        if (type(val) is not list) or len(val) < 2 < len(val):
            return JsonResponse({'results': 'Invalid Input - Input not a valid coordinate point.'})
        else:
            point_list.append(val)

    results = database.get_entries_in_area(point_list)
    return JsonResponse({'results': results})


def search(request, criteria=None):
    search_array = []
    search_input = str(criteria).split(",")
    for split_input in search_input:
        split_val = split_input.split("=")
        if len(split_val) == 2 and len(split_val[1]) > 0:
            search_array.append(split_val)

    rtn = {}
    if len(search_array) > 0:
        print(search_array)
        for search in search_array:
            search_rslts = database.search_key(search[0], search[1])
            rtn = dict(list(search_rslts.items()) + list(rtn.items()))
    else:
        rtn = database.search(criteria)

    if len(rtn) > 0:
        items = []
        for item in rtn:
            items = items + [json.loads(rtn[item])]
        return JsonResponse({'results': items})
    else:
        return JsonResponse({'results': ''})