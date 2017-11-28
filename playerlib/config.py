#!/usr/bin/env python3

import os
import yaml

class Config:

    default_backend = 'mplayer'
    default_backend_path = '/usr/bin/mplayer'
    default_color_palette = [
        ('head', 'yellow', 'black', '', '#a30', ''),
        ('foot', 'light gray', 'black'),
        ('file', 'white', '', '', '#fff', ''),
        ('file_focused', 'white', 'black', '', '#fff', 'g11'),
        ('dir', 'dark green', '', '', '#8a5', ''),
        ('dir_focused', 'dark green', 'black', '', '#8a5', 'g11'),
        ('error', 'dark red', '', '', '#a00', ''),
        ('info', 'dark cyan', '', '', '#06f', ''),
        ('separator', 'black', 'black', '', 'g16', ''),
    ]
    default_bookmarks_file = os.path.expanduser('~') + '/.config/player/bookmarks.json'

    def __init__(self):
        try:
            with open(os.path.expanduser('~') + '/.config/player/config.yml', 'r') as f:
                config = yaml.load(f.read())
        except: pass

        try: self.backend = config['backend']['name']
        except: self.backend = self.default_backend

        try: self.backend_path = config['backend']['path']
        except: self.backend_path = self.default_backend_path

        try: self.color_palette = config.color_palette
        except: self.color_palette = self.default_color_palette

        try: self.bookmarks_file = config.bookmarks.file
        except: self.bookmarks_file = self.default_bookmarks_file

