# Matterpy - A simple python mattermost bot

![image](https://img.shields.io/github/license/adfinis-sygroup/matterpy.svg?maxAge=2592000)

This bot is purely based on python 3.5 asyncio. All functionality is
provided by plugins.

## Configuration

The configuration is done via .ini file. There are several locations
where matterpy looks for a configuration:

  - /etc/matterpy.ini
  - $HOME/config/matterpy/matterpy.ini
  - matterpy.ini (local to where you start matterpy)

All those files are parsed (if they exist). If a specific config is not
found in one of them, then the next file is checked, and so on.

## Deployment

You can just deploy the code as a python wheel package into a virtualenv
or whatever. Alternateively, there's a Docker image on Dockerhub that
you can use. Just run it with the config file (see below) mounted into
/code/matterpy.ini:

``` sourceCode bash
docker run -ti --rm -v $PWD/matterpy.ini:/code/matterpy.ini adfinissygroup/matterpy
```

## Example config

Here's an example configuration, which configures matterpy to enable
just the "echo" plugin.

``` sourceCode ini
[DEFAULT]
username = matterpy
port     = 8080
host     = your-public-ip-address

[channel testing]
incoming = testing
outgoing = https://your.mattermost.server/hooks/hook-identifier

[plugin matterpy.contrib.echo]

filter = echo
```

## Plugins

Plugins are configured by a `plugin` section in the config file. The
name of the plugin should refer to a loadable / importable python
module, which needs to define a single public function named `init()`.
This will be called upon startup.

The `init()` function will receive a `manager` object as well as it's
configuration in a dict.

You can then call `manager.register(some_callback_function)` to get a
call each time you get an incoming message.

The callback function will receive the full mattermost message as a
dict, and a `reply` (async) function as parameters. A simple echo plugin
could look like this:

``` sourceCode python
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
```

### Echo Plugin

Replies with a quote of what has just been said. Pretty useless, except
for testing and to show as an example. See above for the source :)

### Redmine Plugin

Redmine integration - Show issue details when an issue is mentioned.

Trigger words are: "redmine\#1234" or "rm\#1234" (the hash sign is
optional, spaces are allowd).

The configuration takes the following keys:

``` sourceCode ini
[plugin matterpy.contrib.redmine]
redmine_username = api_username
redmine_password = y0urp@ssw0rd
api_key = oeruilsdfioauseroiusfsf

url     = https://base.url.of.your.redmine
```

### Jira Plugin (Experimental)

Upon mention of a Jira issue (such as FOO-123), queries Jira and
displays details about the given ticket.

REquires the following config:

``` sourceCode ini
[plugin matterpy.contrib.jira]

base_url = http://url.to.your.jira

auth = basic

user = jira_username
pass = jira_password
```

Note that this plugin is still WIP. I still need to convert the title
into a link and convert the description body from textile into markdown
(or devise some other plan to handle it). Also, possibly tons of
stabilisation etc.

### Counter Plugin

This plugin is just a showcase for how to initialize a module
asynchronously, and schedule periodic tasks (ie. does not react to user
input, but some other trigger).

``` sourceCode ini
[plugin matterpy.contrib.counter]

start_at = 1
channel = testing
```

### RSS Plugin

Automaticly posts RSS feeds on an set interval into a Mattermost chat of
your choice.

For multiple RSS feeds add more of the shown blocks.

The interval is configured in seconds. The format configuration is
optional.

With the format configuration you can change how the message looks by
rearranging them to your liking.

``` sourceCode ini
[plugin matterpy.contrib.rss]

feed.1.channel = channel_name
feed.1.url = https://url.to.rss.feed
feed.1.interval = 60
feed.1.format = {title}, {body}, {url}

feed.foo.channel = testing
feed.foo.url = http://url.to.rss.feed
feed.foo.interval = 120
```
