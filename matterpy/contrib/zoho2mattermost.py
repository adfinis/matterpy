#!/usr/bin/env python3


from aiohttp.web import Response


def init(manager, conf):

    async def handle_request(request):

        post_data = await request.post()
        data = {}
        data.update(request.query)
        data.update(post_data)

        message = data.get('message', '')

        await manager.send(
            conf.get('channel'),
            message
        )
        return Response(body=b'ok')

    manager.register_generic_hook(
        'POST',
        conf.get('listen'),
        handle_request
    )

