#!/usr/bin/env python3

import datetime
import logging

import asyncio

import aiocoap.resource as resource
import aiocoap

class MyRespResource(resource.ObservableResource):

    def __init__(self):
        super(MyRespResource, self).__init__()

    @asyncio.coroutine
    def render_get(self, request):
        content = "GET Ma vaffanculo!".encode('ascii')
        response = aiocoap.Message(code=aiocoap.CONTENT, payload=content)
        return response

    @asyncio.coroutine
    def render_post(self, request):
        print('POST payload: %s' % request.payload)
        content = request.payload
        payload = ("Post accepted. Parameter: %r" % content).encode('utf8')
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
