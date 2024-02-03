#!/usr/bin/env python3

# pylint: disable=unused-import
"""
Tool to split Clangen sprites into separate files.
"""

import argparse
import os
import glob

parser = argparse.ArgumentParser(
                    prog='Sprite splitter',
                    description='Splits Clangen sprites')

parser.add_argument('-d', '--delete',
                    action='store_true',
                    help='delete original files')
args = parser.parse_args()

# set default directory for MacOS
directory = os.path.dirname(__file__)
if directory:
    os.chdir(directory)

# don't open pygame window
os.environ['SDL_VIDEODRIVER'] = 'dummy'

from scripts.cat.sprites import sprites
sprites.load_all()

if args.delete:
    for png in glob.glob("sprites/*.png"):
        os.remove(png)
    for png in glob.glob("sprites/faded/*.png"):
        os.remove(png)
    os.rmdir("sprites/faded")
    for png in glob.glob("sprites/paralyzed/*.png"):
        os.remove(png)
    os.rmdir("sprites/paralyzed")
