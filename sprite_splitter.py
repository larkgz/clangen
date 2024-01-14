#!/usr/bin/env python3

# pylint: disable=unused-import
"""
Tool to split Clangen sprites into separate files.
"""

import os

# set default directory for MacOS
directory = os.path.dirname(__file__)
if directory:
    os.chdir(directory)

# don't open pygame window
os.environ['SDL_VIDEODRIVER'] = 'dummy'

from scripts.cat.sprites import sprites
sprites.load_all()
