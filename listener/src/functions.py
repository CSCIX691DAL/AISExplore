from src import postgresql as pgs


# Threading not implemented in these functions due to the
# amount of threads spawned for each implementation,
# easier when done single threaded

# process the message depending on type
def more_processing(result):
    if (result['id'] == 1) or (result['id'] == 2) or (result['id'] == 3):
        location_data = modify_location(result)
        pgs.save_location(location_data)
        pgs.update_identity_from_location(location_data)

        # Thread(target=pgs.save_location, args=(location_data,)).start()
        # Thread(target=pgs.update_identity_from_location, args=(location_data,)).start()
    elif result['id'] == 4:
        station_data = modify_station(result)
        pgs.save_stations(station_data)
    elif result['id'] == 5:
        identity_data = modify_info(result)
        pgs.save_message5(identity_data)


# change the values of the dict to database style values.
def modify_station(data):
    data['lat'] = data.pop('y')
    data['lng'] = data.pop('x')
    data['accuracy'] = data.pop('position_accuracy')
    data['epfd'] = data.pop('fix_type')
    del data['slot_timeout'], data['spare'], data['repeat_indicator']
    del data['transmission_ctl'], data['sync_state'], data['id']
    return data


# change the values of dict to database style values
def modify_info(data):
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
    del data['id'], data['spare'], data['ais_version']
    del data['dte'], data['repeat_indicator']
    return data


# change the values of the dict to database style values
def modify_location(data):
    data['lat'] = data.pop('y')
    data['lng'] = data.pop('x')
    data['speed'] = data.pop('sog')
    data['accuracy'] = data.pop('position_accuracy')
    data['true_heading'] = data.pop('true_heading')
    data['turn'] = data.pop('rot')
    data['course'] = data.pop('cog')
    data['time_stamp'] = data.pop('timestamp')
    del data['repeat_indicator'], data['rot_over_range']
    del data['sync_state'], data['spare'], data['id'], data['raim']
    return data
