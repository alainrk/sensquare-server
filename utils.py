from Query import *
import mgrs
import time
import mgrs
import json
import random

TYPE_AMPLITUDE = 100
TYPE_WIFI = 101
TYPE_TEL = 102
DEFAULT_RADIUS = 999
DEFAULT_TIMEOUT = 999

granToMeters = {5:1, 4:10, 3:100, 2:1000, 1:10000, 0:100000}
granToRadius = {5:1, 4:7, 3:70, 2:700, 1:7000, 0:70000}

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
def belongsto(zone, coord, granularity):
    # Division in "32T PQ 12345 12345"
    gridsq_zone, bigsq_zone, x_zone, y_zone = zone[:3], zone[3:5], zone[5:10], zone[10:15]
    gridsq_coord, bigsq_coord, x_coord, y_coord = coord[:3], coord[3:5], coord[5:10], coord[10:15]
    return gridsq_zone == gridsq_coord and \
            bigsq_zone == bigsq_coord and \
            x_zone[0:granularity] == x_coord[0:granularity] and \
            y_zone[0:granularity] == y_coord[0:granularity]

'''
Return center (latitude, longitude) of mgrs (full coords) given a granularity

Gran 3, 32T PQ 123** 123** ===> 32T PQ 12355 12355 (Half!)
Gran 2, 32T PQ 12*** 12*** ===> 32T PQ 12555 12555 (Half!)

Es:
>>> gran = 3
>>> x = "99999"
>>> pad = "5"*(5-gran)
>>> pad
'50'
>>> x = x[:3]+pad
>>> x
'99950'

'''
def getCenterOfMGRSInCoord(fmgrs, gran):
    try:
        m = mgrs.MGRS()
        if -1 < gran < 5:
            # Division in "32T PQ 12345 12345"
            gridsq_fmgrs, bigsq_fmgrs, x_fmgrs, y_fmgrs = fmgrs[:3], fmgrs[3:5], fmgrs[5:10], fmgrs[10:15]
            pad = "5"*(5-gran)
            x, y = x_fmgrs[:gran]+pad, y_fmgrs[:gran]+pad
            new_mgrs = gridsq_fmgrs + bigsq_fmgrs + x + y
            #print ("\nGran: "+str(gran)+"\n"+fmgrs+"\n"+new_mgrs+"\n")
            return m.toLatLon(str.encode(new_mgrs)) # MGRS Lib accept only bytes!
        else:
            return m.toLatLon(str.encode(fmgrs))
    except Exception as e:
        print ("Exception getCenterOfMGRSInCoord: "+str(e))
        return m.toLatLon(str.encode(fmgrs))

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
        tech, strength, operator, throughput = client_value.split(",")
        queryObj.insertInAllTelData(client_user, client_lat, client_long, mgrs_coord, italytimestamp(), strength, operator, tech, throughput)

    else:
        queryObj.insertInAllSensorData(client_user, client_sensor, client_lat, client_long, mgrs_coord, client_value, italytimestamp())

    queryObj.close()

'''
Returns (radius, timeout) based on rules in DB
'''
def getRadiusAndTimeoutForClient(cuser, csensor, cmgrs):
    # Index field in DB rows
    fMGRS, fTIMEOUT, fGRANSAMPLE = 3, 7, 9
    fStakeID = 2

    # Getting rules
    queryObj = Query()
    rules = list(queryObj.getAllRulesForSensor(csensor))

    # TODO HERE ADD ALSO SEARCH FOR STAKEHOLDERS RULES THAT CLIENT ACCEPTED
    # BEWARE OF FIELD POSITION, DIFFERENT IN STAKEHOLDERS RULES !!!!!!!!!!!!!!

    # Adding them to rules, automatically then we can get the max granularity
    # in time and space for client

    stakeholders_accepted = list( map( lambda x:x[fStakeID], list(queryObj.getSubscriptionByUserAndSensor(cuser, csensor)) ))

    rules_stakeholders = []
    for s in stakeholders_accepted:
      rules_stakeholders += list(queryObj.getAllStakeholdersRulesForSensor(csensor, s))
    rules += rules_stakeholders

    queryObj.close()

    belongs = list(filter(lambda r:belongsto(r[fMGRS], cmgrs, r[fGRANSAMPLE]), rules))
    #print(belongs)

    if belongs:
        # Radius from max granularity or default
        finest = max(belongs, key=lambda x:x[fGRANSAMPLE])
        c_lat, c_long = getCenterOfMGRSInCoord(finest[fMGRS], finest[fGRANSAMPLE])
        radius = granToRadius[finest[fGRANSAMPLE]]

        # Timeout from min sampled
        samplest = min(belongs, key=lambda x:x[fTIMEOUT])
        timeout = samplest[fTIMEOUT]
    else:
        c_lat, c_long = None, None
        radius, timeout = DEFAULT_RADIUS, DEFAULT_TIMEOUT

    return (c_lat, c_long, radius, timeout)






















# print(belongto("32TPQ1234512345", "32TPQ1238912389", 4)) # False
# print(belongto("32TPQ1234512345", "32TPQ1238912389", 2)) # True
