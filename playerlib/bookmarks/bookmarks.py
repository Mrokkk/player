#!/usr/bin/env python3

import os
import urwid

from playerlib.helpers.header import *
from playerlib.helpers.helpers import *
from playerlib.helpers.scrollable_listbox import *
from .bookmark import *

class Bookmarks(urwid.WidgetWrap):

    footer_text = 'Bookmarks'

    def __init__(self, config, command_handler):
        self.bookmarks_file = config.bookmarks_file
        self.command_handler = command_handler
        self.header = Header('Bookmarks')
        self.content = urwid.SimpleListWalker([self.header])
        self._load_bookmarks()
        self.listbox = ScrollableListBox(self.content)
        super().__init__(urwid.Frame(self.listbox, footer=urwid.AttrWrap(urwid.Text(self.footer_text), 'foot')))

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

    def unhandled_input(self, key):
        if key == 'enter':
            self._go_to_bookmark(self.listbox.focus)
        else:
            try:
                index = int(key)
                self._go_to_bookmark(self.content[index])
            except: return

