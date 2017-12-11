#!/usr/bin/env python3

import os
import urwid
import urwim
from .bookmark import *

class Bookmarks(urwim.ViewWidget):

    footer_text = 'Bookmarks'

    def __init__(self, config):
        self.bookmarks_file = config.bookmarks_file
        self.header = urwim.Header('Bookmarks')
        self.content = urwid.SimpleListWalker([])
        self._load_bookmarks()
        self.listbox = urwim.ListWidget(self.content)
        callbacks = {
            'enter': self._handle_enter,
            '1': lambda: self._handle_number(1),
            '2': lambda: self._handle_number(2),
            '3': lambda: self._handle_number(3),
            '4': lambda: self._handle_number(4),
            '5': lambda: self._handle_number(5),
            '6': lambda: self._handle_number(6),
            '7': lambda: self._handle_number(7),
            '8': lambda: self._handle_number(8),
            '9': lambda: self._handle_number(9),
            '0': lambda: self._handle_number(10),
        }
        super().__init__(
            self.listbox,
            callbacks,
            self.footer_text,
            header=self.header)

    def _save_bookmarks(self):
        import json
        with open(self.bookmarks_file, 'w') as f:
            json.dump([b.text() for b in self.content], f)

    def _load_bookmarks(self):
        import json
        if os.path.exists(self.bookmarks_file):
            with open(self.bookmarks_file, 'r') as f:
                bookmarks = json.load(f)
                for i, b in enumerate(bookmarks):
                    self.content.append(Bookmark(i + 1, b))

    def add(self, path):
        index = len(self.content)
        self.content.append(Bookmark(index, path))
        self._save_bookmarks()

    def _go_to_bookmark(self, bookmark):
        urwim.App().command_handler(':change_dir {}'.format(bookmark.text()))
        urwim.App().command_handler(':toggle_pane_view')

    def _handle_enter(self):
        self._go_to_bookmark(self.listbox.focus)

    def _handle_number(self, number):
        try:
            self._go_to_bookmark(self.content[number - 1])
        except: urwim.App().command_handler(':error "no such bookmark: {}"'.format(number))

