from datetime import datetime
from threading import Thread

import psycopg2 as pg
import sys
from ais import nmea_queue
from json import dumps

counter = 0


def read_file():
    for line in open('values.csv'):
        yield line


def decode():
    global ais_queue, cursor, counter
    while ais_queue.qsize():
        try:
            result = ais_queue.get()
            if result and 'decoded' in result:
                result = result['decoded']
                if result['id'] == 5:
                    result = modify_dict(result)
                    # print(dumps(result, sort_keys=True, indent=4))
                    Thread(target=save_postgreSQL, args=(cursor, result,)).start()

        except Exception as e:
            print(str(e))


def modify_dict(data):
    data['mmsi'] = data.pop('mmsi')
    data['imo_number'] = data.pop('imo_num')
    data['call_sign'] = data.pop('callsign')
    data['ship_type'] = data.pop('type_and_cargo')
    data['dimension_to_bow'] = data.pop('dim_a')
    data['dimension_to_stern'] = data.pop('dim_b')
    data['dimension_to_port'] = data.pop('dim_c')
    data['dimension_to_starboard'] = data.pop('dim_d')
    data['position_fix_type'] = data.pop('fix_type')
    data['vessel_name'] = data.pop('name')
    del data['md5'], data['id'], data['spare'], data['ais_version'], data['dte'], data['repeat_indicator']
    return data


def save_postgreSQL(psql_handler, values):
    global counter
    query = '''INSERT INTO ais_message5(mmsi, imo_number, vessel_name, destination, call_sign, ship_type,
    position_fix_type, dimension_to_bow, dimension_to_stern, dimension_to_port, dimension_to_starboard, 
    draught, eta_day, eta_hour, eta_minute, eta_month, event_time) 
    VALUES (%s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
    ON CONFLICT (mmsi) DO UPDATE SET 
    imo_number=excluded.imo_number, destination = excluded.destination, 
    call_sign = excluded.call_sign, ship_type = excluded.ship_type,
    position_fix_type = excluded.position_fix_type, dimension_to_bow = excluded.dimension_to_bow,
    dimension_to_stern = excluded.dimension_to_stern, dimension_to_port = excluded.dimension_to_port,
    dimension_to_starboard = excluded.dimension_to_starboard,draught = excluded.draught,
    eta_day = excluded.eta_day,eta_hour = excluded.eta_hour, eta_minute = excluded.eta_minute,
    eta_month = excluded.eta_month,event_time = excluded.event_time;'''

    data = (values['mmsi'], values['imo_number'], values['vessel_name'], values['destination'],
            values['call_sign'], values['ship_type'], values['position_fix_type'], values['dimension_to_bow'],
            values['dimension_to_stern'], values['dimension_to_port'], values['dimension_to_starboard'],
            values['draught'],
            values['eta_day'], values['eta_hour'], values['eta_minute'], values['eta_month'],
            str(datetime.strptime(str(datetime.now()), '%Y-%m-%d %H:%M:%S.%f')))

    psql_handler.execute(query, data)


if __name__ == '__main__':
    try:
        db_connection = pg.connect(
            dbname='collected_ais',
            user='ais_app_user', port="5431",
            password='apPW4197@nxzt')
        db_connection.set_session(autocommit=True)
        cursor = db_connection.cursor()
    except pg.Error:
        print("Error Connecting")
    else:
        print("Connected to PostGRESQL")
        ais_queue = nmea_queue.NmeaQueue()
        for msg in read_file():
            ais_queue.put(msg)
            decode()
            counter = counter + 1
            print('Counter:', counter, end='\r')
