#!/usr/bin/env python3

import os
import re
import urwid
import urwim

class DirEntry(urwim.ListBoxEntry):

    def __init__(self, name, parent_path, is_a_dir=False, level=0):
        self.name = name
        self.parent_path = parent_path
        self.isdir = is_a_dir
        self.level = level
        self.open = False
        if is_a_dir:
            widget = urwid.AttrMap(urwid.SelectableIcon(['  ' * level, u'▸ ', name, '/'], 0),
                'dir', 'dir_focused')
        else:
            widget = urwid.AttrMap(urwid.SelectableIcon(['  ' * level, '  ', name], 0),
                'file', 'file_focused')
        super().__init__(widget)

    @property
    def path(self):
        return os.path.join(self.parent_path, self.name).replace("\\", "\\\\")

    def text(self):
        return self.name

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

