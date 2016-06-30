#!/usr/bin/env python3

from utils import *
import datetime
import logging
import asyncio
import aiocoap.resource as resource
import aiocoap
import signal
import sys
from datetime import datetime


'''
PYTHON 3 NEEDED !!!!!!!!!!!!!!!!!!!
Library mgrs:
pip3 install --user https://pypi.python.org/packages/8a/38/d7824a8a7dd8a181d5da11977f36467429009967296ce23b6911233fe4b0/mgrs-1.3.3.tar.gz
'''

class GetSubscriptions(resource.ObservableResource):

    def __init__(self):
        super(GetSubscriptions, self).__init__()

    @asyncio.coroutine
    def render_post(self, request):
        try:
            ###### INITIALIZE #####
            content = (request.payload).decode('utf8')
            clientdata = json.loads(content)[0] # Just one element in jsonarray received

            ###### RECEIVING ######
            queryObj = Query()
            stakeholders = list(queryObj.getStakeholders())
            subscribedStakeholders = list(queryObj.getSubscribedStakeholders(clientdata['user']))

            subIds = list(map(lambda x:x[0], subscribedStakeholders))
            queryObj.close()

            ###### SENDING ######
            jsonarr = []
            for s in stakeholders:
                data = {}
                print(s)
                data['id'] = s[0]
                data['name'] = s[1]
                data['subscribed'] = 1 if s[0] in subIds else 0
                jsonarr.append(data)

            json_arr = json.dumps(jsonarr)
            json_obj = json.dumps(data)

            bytereprArr = str.encode(json_arr)
            bytereprObj = str.encode(json_obj)

            return aiocoap.Message(code=aiocoap.CONTENT, payload=bytereprArr)

        except Exception as e:
            print ("Exception MAIN: "+str(e))
            return aiocoap.Message(code=aiocoap.CONTENT, payload=b'[]')


class UpdateSubscription(resource.ObservableResource):

    def __init__(self):
        super(UpdateSubscription, self).__init__()

    @asyncio.coroutine
    def render_post(self, request):
        try:
            ###### INITIALIZE #####
            content = (request.payload).decode('utf8')

            ###### RECEIVING ######
            clientdata = json.loads(content)
            cuser = clientdata[0]['user']

            queryObj = Query()
            stakeholders = queryObj.deleteAllSubscriptionForUser(cuser)
            for subscription in clientdata[1:]:
                # TODO: Currently insert for each sensor
                queryObj.insertSubscription(cuser, subscription['id'], 5)
                queryObj.insertSubscription(cuser, subscription['id'], 6)
                queryObj.insertSubscription(cuser, subscription['id'], 12)
                queryObj.insertSubscription(cuser, subscription['id'], 13)
                queryObj.insertSubscription(cuser, subscription['id'], 100)
                queryObj.insertSubscription(cuser, subscription['id'], 101)
                queryObj.insertSubscription(cuser, subscription['id'], 102)
            queryObj.close()

            return aiocoap.Message(code=aiocoap.CONTENT, payload=b"")

        except Exception as e:
            print ("Exception MAIN: "+str(e))
            return aiocoap.Message(code=aiocoap.CONTENT, payload=b'[]')


class SensingSend(resource.ObservableResource):

    def __init__(self):
        super(SensingSend, self).__init__()

    @asyncio.coroutine
    def render_post(self, request):
        try:
            ###### INITIALIZE #####
            random.seed(time.time())
            mgrs_instance = mgrs.MGRS()

            ###### RECEIVING ######
            content = (request.payload).decode('utf8')
            clientdata = json.loads(content)[0] # Only one sensor per request
            #print ("Received ", clientdata)

            ###### SAVE in DB ######
            saveData(clientdata)

            ##### GET THE RULES #####
            cuser, csensor, clatitude, clongitude = clientdata['user'], clientdata['sensor'], clientdata['lat'], clientdata['long']
            cmgrs = mgrs_instance.toMGRS(clatitude, clongitude)
            center_lat, center_long, radius, timeout = getRadiusAndTimeoutForClient(cuser, csensor, cmgrs.decode("utf-8")) # Avoid b'string'

            ###### SENDING ######
            jsonarr = []
            data = {}
            data['timeout'] = timeout
            data['sensor'] = csensor
            data['lat'] = center_lat if center_lat else clatitude
            data['long'] = center_long if center_long else clatitude
            data['radius'] = radius

            jsonarr.append(data)

            json_arr = json.dumps(jsonarr)
            json_obj = json.dumps(data)

            bytereprArr = str.encode(json_arr)
            bytereprObj = str.encode(json_obj)

            return aiocoap.Message(code=aiocoap.CONTENT, payload=bytereprArr)

        except Exception as e:
            print ("Exception MAIN: "+str(e))
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
    root.add_resource(('sensing_send',), SensingSend())
    root.add_resource(('get_subscriptions',), GetSubscriptions())
    root.add_resource(('update_subscriptions',), UpdateSubscription())
    asyncio.async(aiocoap.Context.create_server_context(root))
    asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    main()
