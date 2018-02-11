#!/usr/bin/env python3

import os
import yaml
import logging
from urwim import log_exception, YamlConfigReader, JsonConfigReader

class obj:
    def __init__(self, d):
        for a, b in d.items():
            if isinstance(b, (list, tuple)):
               setattr(self, a, [obj(x) if isinstance(x, dict) else x for x in b])
            else:
               setattr(self, a, obj(b) if isinstance(b, dict) else b)

    def __repr__(self):
        return str(self.__dict__)

class Config:

    defaults = {
        'backend': {'name': 'mplayer', 'path': '/usr/bin/mplayer'},
        'bookmarks': {'path': os.path.expanduser('~') + '/.config/player/bookmarks.json'},
        'colors': 256,
        'color_palette': [
            ('head', 'yellow', 'black', '', '#a30', ''),
            ('foot', 'light gray', 'black', '', '', 'g11'),
            ('file', 'white', '', '', '#fff', ''),
            ('file_focused', 'white', 'black', '', '#fff', 'g11'),
            ('dir', 'dark green', '', '', '#8a5', ''),
            ('dir_focused', 'dark green', 'black', '', '#8a5', 'g11'),
            ('error', 'dark red', '', '', '#a00', ''),
            ('info', 'dark cyan', '', '', '#06f', ''),
            ('separator', 'black', 'black', '', 'g16', ''),
            ('tab_inactive', '', '', '', '', ''),
            ('tab_active', 'black', 'blue', '', '#000', '#0ad'),
        ]
    }

    def __init__(self):
        config = Config.defaults.copy()
        path = os.path.expanduser('~/.config/player/config.yml')
        if os.path.exists(path):
            yaml_config = YamlConfigReader().read(path)
            if yaml_config:
                config.update(yaml_config)
        c = obj(config)
        logging.debug(c)
        self.backend = os.path.expanduser(c.backend.name)
        self.backend_path = os.path.expanduser(c.backend.path)
        self.bookmarks_file = os.path.expanduser(c.bookmarks.path)
        try: self.color_palette = self._create_palette(config['palette'])
        except: self.color_palette = self.defaults['color_palette']
        self.colors = c.colors


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
        for name in ('head', 'foot', 'file', 'file_focused', 'dir', 'dir_focused', 'error', 'info', 'separator', 'tab_inactive', 'tab_active'):
            try: color_palette.append(self._create_palette_entry(256, name, palette))
            except:
                log_exception(logging)
                color_palette.append((name, '', '', '', '', ''))
        return color_palette

