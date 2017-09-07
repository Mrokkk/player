#!/usr/bin/env python3

import os
import urwid

import config

class HorizontalPanes(urwid.Columns):

    def __init__(self, widgets):
        super().__init__([], dividechars=1)
        self.contents.append((widgets[0], self.options('weight', 50)))
        self.contents.append((widgets[1], self.options('weight', 50)))
        self.set_focus(0)

    def keypress(self, size, key):
        return self.focus.keypress(size, key)

    def unhandled_input(self, key):
        return self.focus.unhandled_input(key)

    def search_forward(self, pattern):
        return self.focus.search_forward(pattern)

    def search_backward(self, pattern):
        return self.focus.search_backward(pattern)

    def switch_focus(self):
        self.set_focus(0 if self.focus_position else 1)

