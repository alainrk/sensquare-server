#!/usr/bin/env python3

import datetime
import logging
import asyncio
import aiocoap.resource as resource
import aiocoap
import mgrs
import json
import random
import time
import signal
import sys
from Query import *
from datetime import datetime


'''

PYTHON 3 NEEDED !!!!!!!!!!!!!!!!!!!

Library mgrs:

pip3 install --user https://pypi.python.org/packages/8a/38/d7824a8a7dd8a181d5da11977f36467429009967296ce23b6911233fe4b0/mgrs-1.3.3.tar.gz

>>> latitude = 42.0
>>> longitude = -93.0

>>> m = mgrs.MGRS()
>>> c = m.toMGRS(latitude, longitude)
>>> c
'15TWG0000049776'

>>> d = m.toLatLon(c)
>>> d
(41.999997975127997, -93.000000000000014)

'''

TYPE_AMPLITUDE = 100;
TYPE_WIFI = 101;
TYPE_TEL = 102;

'''
Name, MGRS Filter, TypeNum
Light|12|5
Pressure|8|6
Humidity|11|12
Temperature|10|13
Audio Amplitude|12|100
WiFi|13|101
Tel|13|102

Usage for filter:
>>> a="AAAAABBBBBCCCCC"  ==> Length: 15
>>> a[:13]
'AAAAABBBBBCCC'          ==> Length: 13
'''
mgrs_mask = {5:12, 6:8, 12:11, 13:10, 100:12, 101:13, 102:13}

def italytimestamp(legal=True):
    return int(time.time() + (2 if legal else 1)*3600)

class MyRespResource(resource.ObservableResource):

    def __init__(self):
        super(MyRespResource, self).__init__()

    @asyncio.coroutine
    def render_get(self, request):
        content = "GET Not supported!".encode('ascii')
        response = aiocoap.Message(code=aiocoap.CONTENT, payload=content)
        return response

    @asyncio.coroutine
    def render_post(self, request):
        try:
            random.seed(time.time())

            ###### RECEIVING ######
            content = (request.payload).decode('utf8')
            clientdata = json.loads(content)[0] # Only one sensor per request
            #print (clientdata)

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
                    print(bssid, ssid, strength)
                    queryObj.insertInAllWifiData(client_user, ssid, client_lat, client_long, mgrs_coord, bssid, strength, italytimestamp())

            elif client_sensor == TYPE_TEL:
                tech, strength, operator = client_value.split(",")
                print(tech, strength, operator)
                queryObj.insertInAllTelData(client_user, client_lat, client_long, mgrs_coord, italytimestamp(), strength, operator, tech)

            else:
                queryObj.insertInAllSensorData(client_user, client_sensor, client_lat, client_long, mgrs_coord, client_value, italytimestamp())

            queryObj.close()

            ###### SENDING ######
            jsonarr = []
            data = {}
            data['timeout'] = random.randint(3000, 6000)    # TODO: Calculate timeout based on fresh/compl/.. in DB
            data['sensor'] = client_sensor              # Obviously the same arrived
            data['lat'] = client_lat                    # I think the same arrived
            data['long'] = client_long                  # I think the same arrived
            data['radius'] = random.randint(100, 200)   # TODO: Calculate radius from MGRS, and based on data in DB

            jsonarr.append(data)

            json_arr = json.dumps(jsonarr)
            json_obj = json.dumps(data)

            bytereprArr = str.encode(json_arr)
            bytereprObj = str.encode(json_obj)

            return aiocoap.Message(code=aiocoap.CONTENT, payload=bytereprArr)

        except Exception as e:
            print (str(e))
            return aiocoap.Message(code=aiocoap.CONTENT, payload=b'[]')

def handler(signum, frame):
    print('\n\nServer killed!\n')
    sys.exit(0)

def main():
    # Kill catch
    signal.signal(signal.SIGTERM, handler)
    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGQUIT, handler)
    signal.signal(signal.SIGABRT, handler)

    # Resource tree creation
    root = resource.Site()
    #root.add_resource(('.well-known', 'core'), resource.WKCResource(root.get_resources_as_linkheader))
    root.add_resource(('myresp',), MyRespResource())
    asyncio.async(aiocoap.Context.create_server_context(root))
    asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    main()
