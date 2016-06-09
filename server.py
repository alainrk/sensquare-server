#!/usr/bin/env python3

import datetime
import logging
import asyncio
import aiocoap.resource as resource
import aiocoap
import mgrs

'''

PYTHON 3 NEEDED !!!!!!!!!!!!!!!!!!!

Library mgrs:

pip3 install --user https://pypi.python.org/packages/8a/38/d7824a8a7dd8a181d5da11977f36467429009967296ce23b6911233fe4b0/mgrs-1.3.3.tar.gz

'''

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
        #print('POST payload: %s' % request.payload)
        content = (request.payload).decode('utf8')
        print (content)
        payload = ("Server ACK. Req: %r" % content).encode('utf8')
        return aiocoap.Message(code=aiocoap.CONTENT, payload=payload)


def main():
    # Resource tree creation
    root = resource.Site()
    root.add_resource(('.well-known', 'core'), resource.WKCResource(root.get_resources_as_linkheader))
    root.add_resource(('myresp',), MyRespResource())
    asyncio.async(aiocoap.Context.create_server_context(root))
    asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    main()
