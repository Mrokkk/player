#!/usr/bin/env python3

import os
import yaml
import logging
from playerlib.helpers.helpers import *

class Config:

    default_backend = 'mplayer'
    default_backend_path = '/usr/bin/mplayer'
    default_bookmarks_file = os.path.expanduser('~') + '/.config/player/bookmarks.json'
    default_color_palette = [
        ('head', 'yellow', 'black', '', '#a30', ''),
        ('foot', 'light gray', 'black', '', '', 'g11'),
        ('file', 'white', '', '', '#fff', ''),
        ('file_focused', 'white', 'black', '', '#fff', 'g11'),
        ('dir', 'dark green', '', '', '#8a5', ''),
        ('dir_focused', 'dark green', 'black', '', '#8a5', 'g11'),
        ('error', 'dark red', '', '', '#a00', ''),
        ('info', 'dark cyan', '', '', '#06f', ''),
        ('separator', 'black', 'black', '', 'g16', ''),
    ]


    def __init__(self):
        config = {}
        try:
            with open(os.path.expanduser('~') + '/.config/player/config.yml', 'r') as f:
                config = yaml.load(f.read())
        except: log_exception(logging)
        logging.debug(config)

        try: self.backend = config['backend']['name']
        except: self.backend = self.default_backend

        try: self.backend_path = os.path.expanduser(config['backend']['path'])
        except: self.backend_path = self.default_backend_path

        try: self.colors = config['colors']
        except: self.colors = 256

        try:
            self.color_palette = self._create_palette(config['palette'])
        except:
            self.color_palette = self.default_color_palette
        logging.debug(self.color_palette)

        try: self.bookmarks_file = os.path.expanduser(config['bookmarks']['path'])
        except: self.bookmarks_file = self.default_bookmarks_file


    def _convert_color(self, color):
        if isinstance(color, int):
            return ''.join(['#', hex(color)[2:].rjust(3, '0')])
        return color


    def _create_palette_entry(self, colors, entry, palette):
        # TODO: add support for other color depth
        name = palette[entry]
        try: fg = self._convert_color(name['fg'])
        except: fg = ''
        try: bg = self._convert_color(name['bg'])
        except: bg = ''
        return (entry, '', '', '', fg, bg)


    def _create_palette(self, palette):
        color_palette = []
        for name in ('head', 'foot', 'file', 'file_focused', 'dir', 'dir_focused', 'error', 'info', 'separator'):
            try: color_palette.append(self._create_palette_entry(256, name, palette))
            except:
                log_exception(logging)
                color_palette.append((name, '', '', '', '', ''))
        return color_palette

