from Query import *
import mgrs
import time
import mgrs
import json
import random

TYPE_AMPLITUDE = 100;
TYPE_WIFI = 101;
TYPE_TEL = 102;

'''
@zone, Full coord mgrs (1m precision, even though granularity then will cut)
@granularity, How many "bit" (0-5 => 100km-1m) in 2 last part of mgrs save for match
@coord, Full coord mgrs to check belonging to @zone

Granularity:
0 -> 100.000 m
1 -> 10.000 m
2 -> 1.000 m
3 -> 100 m
4 -> 10 m
5 -> 1 m

Zone given =        "32T PQ 12345 12345"
Coord given =       "32T PQ 12389 12389"
granularity 10m =>      4 (1234* 1234*)     DOES NOT MATCH
granularity 1000m =>    2 (12*** 12***)     MATCH
'''
def belongto(zone, coord, granularity):
    # Division in "32T PQ 12345 12345"
    gridsq_zone, bigsq_zone, x_zone, y_zone = zone[:3], zone[3:5], zone[5:10], zone[10:15]
    gridsq_coord, bigsq_coord, x_coord, y_coord = coord[:3], coord[3:5], coord[5:10], coord[10:15]
    return gridsq_zone == gridsq_coord and \
            bigsq_zone == bigsq_coord and \
            x_zone[0:granularity] == x_coord[0:granularity] and \
            y_zone[0:granularity] == y_coord[0:granularity]


def italytimestamp(legal=True):
    return int(time.time() + (2 if legal else 1)*3600)


def saveData(clientdata):
    client_user = clientdata['user']
    client_time = clientdata['time'] # NOT USED
    client_lat = clientdata['lat']
    client_long = clientdata['long']
    client_sensor = clientdata['sensor']
    client_value = clientdata['value']

    # TODO: Database and logic stuff
    m = mgrs.MGRS()
    mgrs_coord = m.toMGRS(client_lat, client_long)

    queryObj = Query()

    if client_sensor == TYPE_WIFI:
        bssid, ssid, strength = client_value.split(",")
        if not bssid.startswith("00:00:00:00"): # No wifi connected
            queryObj.insertInAllWifiData(client_user, ssid, client_lat, client_long, mgrs_coord, bssid, strength, italytimestamp())

    elif client_sensor == TYPE_TEL:
        tech, strength, operator = client_value.split(",")
        queryObj.insertInAllTelData(client_user, client_lat, client_long, mgrs_coord, italytimestamp(), strength, operator, tech)

    else:
        queryObj.insertInAllSensorData(client_user, client_sensor, client_lat, client_long, mgrs_coord, client_value, italytimestamp())

    queryObj.close()

'''
Returns (radius, timeout) based on rules in DB
'''
def getRadiusAndTimeoutForClient(csensor, cmgrs):
    return random.randint(30, 60), random.randint(50, 100)


# print(belongto("32TPQ1234512345", "32TPQ1238912389", 4)) # False
# print(belongto("32TPQ1234512345", "32TPQ1238912389", 2)) # True
