#!/usr/bin/env python3

from aiohttp import ClientSession
import json
from functools import partial
import importlib
import asyncio


class Manager():

    def __init__(self, conf):
        self.conf = conf
        self.plugins = []
        self.load_plugins()

    def load_plugins(self):
        for name, plugin_conf in self.conf.plugins():
            self.load_plugin(name, plugin_conf)

    def load_plugin(self, name, plugin_conf):
        try:
            print("Initializing module %s" % name)
            mod = importlib.import_module(name)
            if hasattr(mod, 'init'):
                mod.init(self, plugin_conf)
            elif hasattr(mod, 'ainit'):
                loop = asyncio.get_event_loop()
                loop.call_soon(mod.ainit, self, plugin_conf)
        except Exception as exc:
            print("Error during module init: %s" % str(exc))

    def register(self, plugin):
        self.plugins.append(plugin)

    async def receive(self, channel, data):
        reply = partial(self.send, channel)
        for plugin in self.plugins:
            try:
                await plugin(data, reply)
            except Exception as exc:
                print("Error while handling module: %s %s" % (
                    type(exc), str(exc)))
                pass

    async def send(self, channel, text):
        hook = self.conf.channel_config(channel, 'outgoing')
        headers = {'content-type': 'application/json'}
        data = {
            "text":     text,
            "username": self.conf.channel_config(channel, 'username')
        }

        async with ClientSession() as session:
            await session.post(hook,
                               headers=headers,
                               data=json.dumps(data))
