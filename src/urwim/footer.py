#!/usr/bin/env python3

import urwid

class Footer(urwid.WidgetWrap):

    signals = []

    def __init__(self, name):
        self._name = name
        super().__init__(urwid.AttrMap(urwid.Text(self._name), 'foot'))

    @property
    def text(self):
        return self._name

    @text.setter
    def text(self, text):
        self._name = text
        self._w = urwid.AttrMap(urwid.Text(self._name), 'foot')

