#!/usr/bin/env python3

from matterpy import config, server, manager
import asyncio


def channel_info(conf, channel):
    print(" * %s" % channel)
    url = 'http://%s:%s' % (conf.host(), conf.port())
    hook = conf.channel_config(channel, 'incoming')
    print('    incoming: %s/%s' % (url, hook))
    print('    outgoing: %s' % conf.channel_config(channel, 'outgoing'))


def show_config(conf):
    print("Configured channels:")
    for channel in conf.channels():
        channel_info(conf, channel)


def start():
    conf = config.get_conf()
    show_config(conf)

    operate(conf)


def operate(conf):
    mgr = manager.Manager(conf)
    srv = server.Server(conf, mgr)

    srv.run()

    loop = asyncio.get_event_loop()
    try:
        loop.run_forever()
    except RuntimeError:
        pass
