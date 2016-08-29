"""Setuptools package definition"""

# PLEASE REMOVE UNUSED CODE like CustomInstallCommand if you don't use it

from setuptools import setup
from setuptools import find_packages
from setuptools.command.install import install
import codecs
import os
import sys

version = sys.version_info[0]
if version > 2:
    pass
else:
    pass

__version__  = None
version_file = "matterpy/version.py"
with codecs.open(version_file, encoding="UTF-8") as f:
    code = compile(f.read(), version_file, 'exec')
    exec(code)


with codecs.open('README.rst', 'r', encoding="UTF-8") as f:
    README_TEXT = f.read()

setup(
    name = "matterpy",
    version = __version__,
    packages = find_packages(),
    entry_points = {
        'console_scripts': [
              'matterpy=matterpy.main:start'
        ]
    },
    install_requires = [
        'aiohttp'
    ],
    author = "Adfinis-SyGroup AG",
    author_email = "https://adfinis-sygroup.ch/",
    description = "matterpy",
    long_description = README_TEXT,
    keywords = "matterpy,mattermost,bot",
    url = "https://adfinis-sygroup.ch/",
    classifiers = [
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: "
        "GNU Affero General Public License v3",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.4",
    ]
)
