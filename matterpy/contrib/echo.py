#!/usr/bin/env python3

_conf = None


def init(manager, conf):
    global _conf
    _conf = conf
    manager.register(handle_msg)


async def handle_msg(msg, reply):
    text = msg['text']
    text = text.replace("\n", "\n> ")
    await reply("Got your message:\n\n > %s\n" % text)
