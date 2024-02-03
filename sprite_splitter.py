#!/usr/bin/env python3

# pylint: disable=unused-import
"""
Tool to split Clangen sprites into separate files.
"""

import os
import glob

# set default directory for MacOS
directory = os.path.dirname(__file__)
if directory:
    os.chdir(directory)

# don't open pygame window
os.environ['SDL_VIDEODRIVER'] = 'dummy'

from scripts.cat.sprites import sprites
sprites.load_all()

for png in glob.glob("sprites/*.png"):
    os.remove(png)
for png in glob.glob("sprites/faded/*.png"):
    os.remove(png)
os.rmdir("sprites/faded")
for png in glob.glob("sprites/paralyzed/*.png"):
    os.remove(png)
os.rmdir("sprites/paralyzed")
