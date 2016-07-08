#!/usr/bin/env python3

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# This file is part of Crowdroid(sense)/Servercoap project, thesis in Crowdsensing.
# Started from part of the Python aiocoap library project.
# Copyright (c) 2012-2014 Maciej Wasilak <http://sixpinetrees.blogspot.com/>,
#               2013-2014 Christian Amsüss <c.amsuess@energyharvesting.at>
# Copyright (C) 2016 Alain Di Chiappari


import logging
import asyncio
import json

from aiocoap import *

logging.basicConfig(level=logging.INFO)

@asyncio.coroutine
def main():
    protocol = yield from Context.create_client_context()

    jsonarr = []
    data = {}
    data['timestamp'] = 45678976543543242
    data['sensor'] = 4
    data['latitude'] = 45.43543242
    data['longitude'] = 11.43543242
    data['value'] = 13.3232

    jsonarr.append(data)

    json_arr = json.dumps(jsonarr)
    json_obj = json.dumps(data)

    bytereprArr = str.encode(json_arr)
    bytereprObj = str.encode(json_obj)

    # coap://127.0.0.1/myresp
    request = Message(code=POST, payload=bytereprArr)
    request.opt.uri_host = '127.0.0.1'
    request.opt.uri_path = ("myresp",)

    try:
        response = yield from protocol.request(request).response
    except Exception as e:
        print('Failed to fetch resource:')
        print(e)
    else:
        print('Result: %s\n%r'%(response.code, response.payload))

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
