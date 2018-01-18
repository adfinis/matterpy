#!/usr/bin/env python3

import asyncio
import feedparser
from collections import defaultdict
from time import gmtime

_conf = None
_mgr = None


def init(manager, conf):
    global _conf
    global _mgr

    _conf = conf
    _mgr = manager

    loop = asyncio.get_event_loop()
    feedsdict = defaultdict(dict)

    for key in _conf:
        if '.' in key:
            keys = key.split('.')
            if len(keys) == 3:
                feedsdict[keys[1]][keys[2]] = _conf.get(key)
            else:
                print("configuration variable name too short: {}".format(key))
    for key in feedsdict:
        loop.create_task(post_rss(feedsdict.get(key)))


async def post_rss(feedinfo):
    last_message = gmtime()
    format_str   = feedinfo.get('format', "[{title}]({url}), {body}")
    channel      = feedinfo.get('channel')
    url          = feedinfo.get('url')

    if not channel:
        print("mimimi no channel!")
        return
    if not url:
        print("mimimi no url!")
        return

    while True:
        feed = feedparser.parse(url)
        entries = sorted(
            feed.entries,
            key=lambda entry: entry.published_parsed
        )
        for entry in entries:
            message = post_to_text(entry, format_str)

            if last_message <= entry.published_parsed:
                await _mgr.send(channel, message)
                last_message = entry.published_parsed

        await asyncio.sleep(int(feedinfo.get('interval', 60)))


def post_to_text(entry, format_string):
    title = entry.title
    url   = entry.link
    body  = entry.description

    return format_string.format(
        title=title, url=url, body=body
    )
