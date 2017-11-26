#!/usr/bin/env python3

import urwid
from playerlib.helpers.helpers import *

class ViewWidget(urwid.WidgetWrap):

    def __init__(self, widget):
        self.callbacks = {}
        super().__init__(widget)

    def unhandled_input(self, key):
        if key in self.callbacks:
            self.callbacks[key]()

    def searchable_list(self):
        raise NotImplementedError('widget does not support searching')

