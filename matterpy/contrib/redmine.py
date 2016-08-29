#!/usr/bin/env python3

"""
Redmine integration - Show issue details when an issue is mentioned.

Trigger words are: "redmine#1234" or "rm#1234" (the hash sign is optional,
spaces are allowd).

The configuration takes the following keys:

.. code:: ini

   [plugin matterpy.contrib.redmine]
   redmine_username = api_username
   redmine_password = y0urp@ssw0rd
   api_key = oeruilsdfioauseroiusfsf

   url     = https://base.url.of.your.redmine

"""

from aiohttp import ClientSession, BasicAuth
import re

_conf = None


REGEXPS = [
    r'redmine\s*#?\s*(\d+)',
    r'rm\s*#?\s*(\d+)',
]


def init(manager, conf):
    global _conf
    _conf = conf
    manager.register(handle_msg)


async def handle_msg(msg, reply):
    text = msg['text']

    issue_id = id_from_text(text)

    if issue_id is None:
        return

    issue = await get_issue(issue_id)

    if issue:
        message = issue_to_text(issue)
        await reply(message)


def id_from_text(text):
    for regex in REGEXPS:
        match = re.match(regex, text, re.I | re.M | re.S)

        if match:
            return int(match.group(1))


async def get_issue(issue_id):

    issue_url = '%s/issues/%s.json' % (_conf['url'], issue_id)

    if 'redmine_username' in _conf:
        auth = BasicAuth(
            _conf['redmine_username'].strip(),
            _conf['redmine_password'].strip())
    else:
        auth = None

    headers = {
        'Accept': 'application/json',
        'X-Redmine-API-Key': _conf['api_key'].strip()
    }
    async with ClientSession() as session:
        resp = await session.get(issue_url, headers=headers, auth=auth)

        return await resp.json()


def issue_to_text(issue):
    subj = issue['issue']['subject']
    body = textile_to_markdown(issue['issue']['description'])
    id_   = issue['issue']['id']

    issue_url = '%s/issues/%s' % (_conf['url'], id_)

    heading_line = '**[#%s - %s](%s)**\n\n' % (id_, subj, issue_url)

    return "%s\n\n%s" % (heading_line, body)


def textile_to_markdown(text):
    text = text.replace('^h1', '#')
    text = text.replace('^h2', '##')
    text = text.replace('^h3', '###')
    text = text.replace('^h4', '####')
    return text
