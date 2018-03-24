#!/usr/bin/env python3
import os

for filename in os.listdir('/home/tblazek/Documents/pygame/item_icons'):
#    if not filename.endswith('.png') and not filename.endswith('.py'):
    if filename.endswith('.png.png') or filename.endswith('.py.png'):
        os.popen('mv {} {}'.format(filename, filename[0:len(filename)-4]))
