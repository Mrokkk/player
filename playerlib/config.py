#!/usr/bin/env python3

import os

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
        import importlib.machinery
        try:
            config = importlib.machinery.SourceFileLoader('config', os.path.expanduser('~') + '/.config/player/config').load_module()
        except:
            config = importlib.machinery.SourceFileLoader('config', os.path.expanduser('~') + '/.playerc').load_module()

        try: self.backend = config.backend
        except: self.backend = self.default_backend

        try: self.backend_path = config.backend_path
        except: self.backend_path = self.default_backend_path

        try: self.color_palette = config.color_palette
        except: self.color_palette = self.default_color_palette

        try: self.bookmarks_file = config.bookmarks_file
        except: self.bookmarks_file = self.default_bookmarks_file

