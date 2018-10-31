#!/usr/bin/env python3

from aiohttp import web
from functools import partial


class Server():

    def __init__(self, conf, manager):
        self.manager = manager
        self.conf    = conf
        self.app     = web.Application()

        self.setup_incoming()

    def setup_incoming(self):
        for channel in self.conf.channels():
            identifier = self.conf.channel_config(channel, 'incoming')

            self.app.router.add_route('POST',
                                      '/%s' % identifier,
                                      partial(self.handle, channel))

    def setup_generic(self, hooks):
        """
        Setup generic webhook callbacks.

        Those should be fed in from the manager in the form of a dict:
        {(method, url): callback}
        """
        for ((method, url), callback) in hooks.items():
            print(" Generic route: %s" % url)
            self.app.router.add_route(
                method,
                url,
                callback
            )

    def run(self):
        web.run_app(
            self.app,
            host=self.conf.host(),
            port=self.conf.port(),
        )

    async def handle(self, channel, request):
        data = await request.json()
        await self.manager.receive(channel, data)

        return web.Response(body=b'ok')
