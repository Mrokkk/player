#!/usr/bin/env python3

import urwid
from playerlib.helpers.helpers import *
from playerlib.helpers.scrollable_listbox import *

class ViewWidget(urwid.Frame):

    def __init__(self, widget, callbacks, header=None, footer=None):
        self._callbacks = callbacks
        self._widget = widget
        super().__init__(widget, header=header, footer=footer)

    def unhandled_input(self, key):
        if key in self._callbacks:
            self._callbacks[key]()

    def searchable_list(self):
        if self._widget.__class__ == ScrollableListBox: return self._widget
        raise NotImplementedError('view does not support searching')

