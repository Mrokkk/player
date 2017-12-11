#!/usr/bin/env python3

import urwid
import urwim

class Bookmark(urwim.ListBoxEntry):
    def __init__(self, index, path):
        self.index = index
        self._path = path
        super().__init__([str(index), ' ', self._path], 'file', 'file_focused')

    def text(self):
        return self._path

