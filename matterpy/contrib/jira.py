#!/usr/bin/env python3

import re
import json
import base64
import asyncio
from aiohttp import ClientSession

_conf = None

def init(manager, conf):
    global _conf
    _conf = conf
    manager.register(handle_msg)




async def jira_info(ticket_id):
    auth_token = '%s:%s' % (_conf['user'], _conf['pass'])
    print("__auth_token: %s" % auth_token)
    jira_header = {
       'Authorization': 'Basic %s' % base64.b64encode(auth_token.encode('utf-8')).decode('ascii'),
       'Content-Type':  'application/json'
    }
    print("__hdr: %s" % jira_header)

    async with ClientSession() as session:
        info = await session.get(
            '%s/rest/api/2/issue/%s' % (_conf['base_url'], ticket_id),
            headers=jira_header,
        )
        print(
            'REQUEST URL: %s/rest/api/2/issue/%s' % (_conf['base_url'], ticket_id),
        )
        print(
            'REQUEST HEADERS: %s' % jira_header,
        )

        data = await info.json()
        print(data)
        if 'key' not in data:
            return None
        summary = data['fields']['summary']
        body    = data['fields']['description']
        return "## {summary}\n{description}\n".format(**data['fields'])



async def handle_msg(msg, reply):
    text = msg['text']
    print(text)
    patterns = re.findall(r'\b[\w\d]+-\d+\b', text, re.I|re.S|re.M)

    coros = []
    for pat in patterns:
        coros.append(reply(await jira_info(pat)))

    asyncio.gather(*coros)

# vim: set sw=4 ts=4 sts et si:
