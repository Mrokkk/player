#!/usr/bin/env python3

import urwid

class ListBoxEntry(urwid.Button):

    signals = []

    def __init__(self, widget):
        super().__init__('')
        self._w = widget

    def text(self):
        '''Has to be implemented by subclass; used for searching in ListBox'''
        raise NotImplementedError('text() not implemented by widget')

    def keypress(self, size, key):
        '''Ignore key presses'''
        return key

