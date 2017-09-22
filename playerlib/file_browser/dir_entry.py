#!/usr/bin/env python3

import os
import re
import urwid

class DirEntry(urwid.Button):

    signals = []

    def __init__(self, name, parent_path, is_a_dir=False, level=0):
        super().__init__(name)
        self.name = name
        self.parent_path = parent_path
        self.isdir = is_a_dir
        self.level = level
        self.open = False
        if is_a_dir:
            self._w = urwid.AttrMap(urwid.SelectableIcon(['  ' * level, u'▸ ', name, '/'], 0),
                'dir', 'dir_focused')
        else:
            self._w = urwid.AttrMap(urwid.SelectableIcon(['  ' * level, '  ', name], 0),
                'file', 'file_focused')

    def keypress(self, size, key):
        return key

    def path(self):
        return os.path.join(self.parent_path, self.name).replace("\\", "\\\\")

    def __lt__(self, other):
        if self.isdir and not other.isdir: return True
        elif not self.isdir and other.isdir: return False
        if other.name[0].isdigit() and self.name[0].isdigit():
            try:
                a = re.search('[0-9]+', self.name).group(0)
                b = re.search('[0-9]+', other.name).group(0)
                return int(a) < int(b)
            except: pass
        return self.name.lower() < other.name.lower()

