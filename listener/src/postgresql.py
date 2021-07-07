# -*- coding: utf-8 -*-
from datetime import datetime
from threading import Thread

import psycopg2 as pgs


def init_connection():
    db_connection = pgs.connect(
        dbname="collected_ais",
        host="127.0.0.1",
        user='ais_app_user', port=5431,
        password='apPW4197@nxzt')

    db_connection.set_session(autocommit=True)
    db_connection.set_client_encoding('UTF8')
    return db_connection


# Message 5 info contain identification information about a vessel, they
# values of existing ships are updated and if the ship is new, create a new
# ship on the database
def save_message5(values):
    db_connection = init_connection()

    cursor = db_connection.cursor()

    query = ('INSERT INTO ais_message5(mmsi, imo_number, vessel_name, destination, call_sign, ship_type,'
             'position_fix_type, dimension_to_bow, dimension_to_stern, dimension_to_port, dimension_to_starboard,'
             'draught, eta_day, eta_hour, eta_minute, eta_month, event_time)'
             'VALUES (%s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
             'ON CONFLICT (mmsi) DO UPDATE SET '
             'imo_number=excluded.imo_number, destination = excluded.destination,'
             'call_sign = excluded.call_sign, ship_type = excluded.ship_type,'
             'position_fix_type = excluded.position_fix_type, dimension_to_bow = excluded.dimension_to_bow,'
             'dimension_to_stern = excluded.dimension_to_stern, dimension_to_port = excluded.dimension_to_port,'
             'dimension_to_starboard = excluded.dimension_to_starboard,draught = excluded.draught,'
             'eta_day = excluded.eta_day,eta_hour = excluded.eta_hour, eta_minute = excluded.eta_minute,'
             'eta_month = excluded.eta_month,event_time = excluded.event_time;')

    time = str(datetime.strptime(str(datetime.now()), '%Y-%m-%d %H:%M:%S.%f'))

    data = (values['mmsi'], values['imo_number'], values['vessel_name'], values['destination'],
            values['call_sign'], values['ship_type'], values['position_fix_type'], values['dimension_to_bow'],
            values['dimension_to_stern'], values['dimension_to_port'], values['dimension_to_starboard'],
            values['draught'],
            values['eta_day'], values['eta_hour'], values['eta_minute'], values['eta_month'], time)
    cursor.execute(query, data)


# same thing as ^ but for messages type 1,2,3, update location of a ship
# from current values
def update_identity_from_location(values):
    db_connection = init_connection()
    cursor = db_connection.cursor()

    query = ('UPDATE ais_message5 '
             'SET event_time=(%s), longitude=(%s), latitude=(%s) '
             'WHERE mmsi=(%s);')
    try:
        time = str(datetime.strptime(str(datetime.now()), '%Y-%m-%d %H:%M:%S.%f'))
        data = (time, values['lng'], values['lat'], values['mmsi'])
        cursor.execute(query, data)

    except Exception as e:
        print("update_identity_from_location:" + str(e))


# update ais_locations of the ships with regards to the
# identification information of the ship
def update_location(values):
    db_connection = init_connection()

    cursor = db_connection.cursor()

    query_update = (u'UPDATE ais_locations '
                    u'SET speed=(%s), time_stamp=(%s), course=(%s),'
                    u'turn=(%s), accuracy=(%s), longitude=(%s), latitude=(%s),'
                    u'true_heading=(%s), nav_status=(%s)'
                    u'WHERE mmsi=(%s);')

    data_update = (values['speed'], values['time_stamp'], values['course'],
                   values['turn'], values['accuracy'], values['lng'], values['lat'],
                   values['true_heading'], values['nav_status'], values['mmsi'],)

    try:
        cursor.execute(query_update, data_update)
    except Exception as e:
        print("update_location", str(e))


def insert_location(values):
    db_connection = init_connection()

    cursor = db_connection.cursor()

    query_insert = (u'INSERT INTO ais_locations '
                    u'(mmsi, speed, time_stamp, course, turn, accuracy, longitude, '
                    u'latitude, true_heading, nav_status)'
                    u'values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);')
    data_insert = (values['mmsi'], values['speed'], values['time_stamp'], values['course'],
                   values['turn'], values['accuracy'], values['lng'], values['lat'],
                   values['true_heading'], values['nav_status'],)
    try:
        cursor.execute(query_insert, data_insert)
    except Exception as e:
        print("insert_location:", str(e))


def save_location(values):
    db_connection = init_connection()
    cursor = db_connection.cursor()
    ship_mmsi = values['mmsi']
    try:
        cursor.execute(u'SELECT longitude, latitude FROM ais_locations where mmsi=(%s);', (ship_mmsi,))
        if cursor.rowcount:
            current_longitude = values['lng']
            current_latitude = values['lat']
            current_destination, old_longitude, old_latitude = get_destination(ship_mmsi)
            payload = (old_latitude, current_latitude, old_longitude, current_longitude, current_destination)
            Thread(target=update_location, args=(values,)).start()
        else:
            Thread(target=insert_location, args=(values,)).start()
    except Exception as e:
        print("save_location", str(e))


def get_destination(ship_mmsi):
    db_connection = init_connection()

    cursor = db_connection.cursor()
    query = cursor.mogrify("SELECT destination, longitude, latitude from ais_message5 WHERE mmsi=(%s);", (ship_mmsi,))
    cursor.execute(query)
    result = cursor.fetchone()
    destination, old_longitude, old_latitude = None, None, None
    if result:
        destination = result[0]
        old_longitude = result[1]
        old_latitude = result[2]
    return destination, old_longitude, old_latitude


def save_stations(values):
    db_connection = init_connection()

    cursor = db_connection.cursor()
    query = ('INSERT INTO ais_stations(mmsi, year, month, day, hour, minute,'
             ' second, accuracy, epfd, raim,  longitude, latitude)'
             'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
             'ON CONFLICT (mmsi) DO UPDATE SET '
             'year=excluded.year, month=excluded.month, day=excluded.day,'
             'hour = excluded.hour, minute=excluded.minute, second=excluded.second,'
             'accuracy = excluded.accuracy, epfd = excluded.epfd, raim = excluded.raim,'
             'longitude = excluded.longitude, latitude = excluded.latitude;')
    data = (values['mmsi'], values['year'], values['month'], values['day'],
            values['hour'], values['minute'], values['second'], values['accuracy'],
            values['epfd'], values['raim'], values['lng'], values['lat'],)
    cursor.execute(query, data)
