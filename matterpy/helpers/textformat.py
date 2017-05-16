#!/usr/bin/env python3

"""Documentation about the module... may be multi-line"""

import re

def textile_to_markdown(text):
    "Convert textile to markdown"
    text, _ = re.subn(r'^h1\.', '# ',     text, re.MULTILINE)
    text, _ = re.subn(r'^h2\.', '## ',    text, re.MULTILINE)
    text, _ = re.subn(r'^h3\.', '### ',   text, re.MULTILINE)
    text, _ = re.subn(r'^h4\.', '#### ',  text, re.MULTILINE)
    return text

