#!/usr/bin/env python3

import urwid

from playerlib.helpers.listbox_entry import *

class Bookmark(ListBoxEntry):
    def __init__(self, index, path):
        self.index = index
        self._path = path
        super().__init__(urwid.AttrMap(urwid.SelectableIcon([str(index), ' ', self._path], 0),
            'file', 'file_focused'))

    def text(self):
        return self._path

