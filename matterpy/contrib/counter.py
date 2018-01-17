#!/usr/bin/env python3

import asyncio

_conf  = None
_mgr   = None


async def ainit(manager, conf):
    global _conf
    global _mgr

    _conf = conf
    _mgr  = manager

    loop = asyncio.get_event_loop()
    await loop.create_task(do_count())


async def do_count():
    count = int(_conf['start_at'])

    while True:
        await _mgr.send(_conf.get('channel'), "%d" % count)
        count += 1
        await asyncio.sleep(1)

