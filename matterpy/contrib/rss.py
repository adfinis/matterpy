#!/usr/bin/env python3

import asyncio
import feedparser
from collections import defaultdict
from time import gmtime

_conf = None
_mgr = None


class WrongKey(Exception):
    pass


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
                print("Configuration variable name too short: {}".format(key))
    for key in feedsdict:
        loop.create_task(post_rss(feedsdict.get(key)))


async def post_rss(feedinfo):
    last_message = gmtime()
    format_str   = feedinfo.get('format', "### [{title}]({url})\n\n{body}")
    channel      = feedinfo.get('channel')
    url          = feedinfo.get('url')

    if not channel:
        print("Please specify a Channel!")
        return
    if not url:
        print("Please specify a URL!")
        return

    seen_urls = []

    while True:
        try:
            feed = feedparser.parse(url)

            updated = lambda entry: entry.get(
                'published_parsed', entry.get('updated_parsed', gmtime())
            )

            entries = sorted(
                feed.entries,
                key=updated
            )

            try:
                for entry in entries:
                    upd = updated(entry)
                    message = post_to_text(entry, format_str)

                    if last_message <= upd and entry.link not in seen_urls:
                        seen_urls.append(entry.link)
                        await _mgr.send(channel, message)

                        last_message = upd

            except WrongKey:
                await _mgr.send(
                    channel, 'There\'s an problem with your Configuration.'
                )
                break

            # only keep 50 "seen" entries
            while len(seen_urls) > 50:
                seen_urls.pop(0)

            await asyncio.sleep(int(feedinfo.get('interval', 60)))

        except Exception as e:
            print("An Error occured:")
            print(e)
            await _mgr.send(channel, "There was an Error: {}".format(e))
            break


def post_to_text(entry, format_string):
    try:
        return format_string.format(
            url = entry.link,
            body = entry.summary,
            **entry
        )

    except KeyError as key_err:
        print('The key {} you defined in the format option does not exist in this feed.'.format(key_err))
        print('Availabe Keys are: ')
        print('url\nbody')
        for key in entry:
            print(key)

        raise WrongKey
