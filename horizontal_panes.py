#!/usr/bin/env python3

import os
import urwid

import config

class HorizontalPanes(urwid.Columns):

    def __init__(self, widgets):
        super().__init__([], dividechars=1)
        self._open_box(widgets[0])
        self._open_box(widgets[1])

    def _open_box(self, box):
        if self.contents:
            del self.contents[self.focus_position + 1:]
        self.contents.append((box, self.options('weight', 50)))
        self.focus_position = len(self.contents) - 1

    def keypress(self, size, key):
        if key == 'ctrl w':
            self.set_focus(0 if self.focus_position else 1)
            return None
        return self.focus.keypress(size, key)

