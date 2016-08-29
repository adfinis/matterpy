
Matterpy - A simple python mattermost bot
=========================================

This bot is purely based on python 3.5 asyncio. All functionality is provided by plugins.


Configuration
-------------

The configuration is done via .ini file. There are several locations where matterpy looks
for a configuration:

* /etc/matterpy.ini
* $HOME/config/matterpy/matterpy.ini
* matterpy.ini (local to where you start matterpy)

All those files are parsed (if they exist). If a specific config is not found
in one of them, then the next file is checked, and so on.

Example config
--------------

Here's an example configuration, which configures matterpy to enable just the
"echo" plugin.

.. code:: ini

   [DEFAULT]
   username = matterpy
   port     = 8080
   host     = your-public-ip-address

   [channel testing]
   incoming = testing
   outgoing = https://your.mattermost.server/hooks/hook-identifier

   [plugin matterpy.contrib.echo]

   filter = echo


Plugins
-------

Plugins are configured by a :code:`plugin` section in the config file. The name of the
plugin should refer to a loadable / importable python module, which needs to define
a single public function named :code:`init()`. This will be called upon startup.

The :code:`init()` function will receive a :code:`manager` object as well as
it's configuration in a dict.

You can then call :code:`manager.register(some_callback_function)` to get a call each
time you get an incoming message.

The callback function will receive the full mattermost message as a dict, and a
:code:`reply` (async) function as parameters. A simple echo plugin could look like this:


.. code:: python

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


Echo Plugin
~~~~~~~~~~~

Replies with a quote of what has just been said. Pretty useless, except for
testing and to show as an example. See above for the source :)


Redmine Plugin
~~~~~~~~~~~~~~


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
