#!/usr/bin/env python3

import os
import configparser


CONFIG_FILES = [
    '/etc/matterpy.ini',
    os.path.expanduser('~/config/matterpy/matterpy.ini'),
    'matterpy.ini',
]


class Config(configparser.ConfigParser):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, interpolation=None, **kwargs)
        self.read(CONFIG_FILES)

    def config(self, group, key):
        return self.get(group, key)

    def channel_config(self, name, key):
        try:
            return self.config('channel %s' % name, key)
        except:
            return self.config('DEFAULT', key)

    def channels(self):
        return [
            section.replace('channel ', '')
            for section in self.sections()
            if section.startswith('channel ')
        ]

    def getdefault(self, group, key, default):
        try:
            return self.get(group, key)
        except configparser.NoOptionError:
            return default

    def host(self):
        return self.getdefault('DEFAULT', 'host', '0.0.0.0')

    def port(self):
        return int(self.getdefault('DEFAULT', 'port', 8080))

    def plugins(self):
        return [
            (section.replace('plugin ', ''),
                {k: v for k, v in self.items(section)})

            for section in self.sections()
            if section.startswith('plugin ')
        ]

_config = None
_config_args = None
_config_kwargs = None


def get_conf(*args, **kwargs):
    global _config
    global _config_args
    global _config_kwargs

    if _config is None:
        _config = Config(*args, **kwargs)
        _config_args = args
        _config_kwargs = kwargs
        return _config

    else:
        assert args == _config_args
        assert kwargs == _config_kwargs
        return _config
