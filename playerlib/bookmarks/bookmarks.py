#!/usr/bin/env python3

import os
import urwid

from playerlib.helpers.header import *
from playerlib.helpers.helpers import *
from playerlib.helpers.scrollable_listbox import *
from playerlib.helpers.view_widget import *
from .bookmark import *

class Bookmarks(ViewWidget):

    footer_text = 'Bookmarks'

    def __init__(self, config, command_handler):
        self.bookmarks_file = config.bookmarks_file
        self.command_handler = command_handler
        self.header = Header('Bookmarks')
        self.content = urwid.SimpleListWalker([self.header])
        self._load_bookmarks()
        self.listbox = ScrollableListBox(self.content)
        super().__init__(urwid.Frame(self.listbox, footer=urwid.AttrWrap(urwid.Text(self.footer_text), 'foot')))
        self.callbacks = {
            'enter': self._handle_enter,
            '1': lambda: self._handle_number(1),
            '2': lambda: self._handle_number(1),
            '3': lambda: self._handle_number(3),
            '4': lambda: self._handle_number(4),
            '5': lambda: self._handle_number(5),
            '6': lambda: self._handle_number(6),
            '7': lambda: self._handle_number(7),
            '8': lambda: self._handle_number(8),
            '9': lambda: self._handle_number(9),
            '0': lambda: self._handle_number(10),
        }

    def _save_bookmarks(self):
        import json
        with open(self.bookmarks_file, 'w') as f:
            json.dump([b.path for b in self.content if b.__class__ == self.Bookmark], f)

    def _load_bookmarks(self):
        import json
        if os.path.exists(self.bookmarks_file):
            with open(self.bookmarks_file, 'r') as f:
                bookmarks = json.load(f)
                for i, b in enumerate(bookmarks):
                    self.content.append(Bookmark(i + 1, b))

    def searchable_list(self):
        return self.listbox

    def add(self, path):
        index = len(self.content)
        self.content.append(Bookmark(index, path))
        self._save_bookmarks()

    def _go_to_bookmark(self, bookmark):
        self.command_handler(':change_dir {}'.format(bookmark.path))
        self.command_handler(':toggle_pane_view')

    def _handle_enter(self):
        self._go_to_bookmark(self.listbox.focus)

    def _handle_number(self, number):
        try:
            self._go_to_bookmark(self.content[number])
        except: self.command_handler(':error "no such bookmark: {}"'.format(number))

