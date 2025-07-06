#!/usr/bin/env python3

import json
import logging
import os
import urwim

from .bookmark import *

class Bookmarks(urwim.ViewWidget):

    header_text: str = 'Bookmarks'

    bookmarks_path: str
    header:         urwim.Header
    content:        urwim.SimpleListWalker
    listbox:        urwim.ListWidget

    def __init__(self, config, commands) -> None:
        self.bookmarks_path = config.bookmarks.path
        self._commands = commands
        self.header = urwim.Header(self.header_text)
        self.content = urwim.SimpleListWalker([])
        self._load_bookmarks()
        self.listbox = urwim.ListWidget(
            self.content,
            on_delete=lambda x: self._on_delete(x),
            on_paste=lambda x: self._on_paste(x))
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
            self.header_text,
            callbacks=callbacks,
            header=self.header)

    def _save_bookmarks(self) -> None:
        with open(self.bookmarks_path, 'w') as f:
            json.dump([b.text for b in self.content], f)

    def _load_bookmarks(self) -> None:
        if os.path.exists(self.bookmarks_path):
            with open(self.bookmarks_path, 'r') as f:
                bookmarks = json.load(f)
                for i, b in enumerate(bookmarks):
                    self.content.append(Bookmark(i + 1, b))

    def add(self, path: str) -> None:
        index = len(self.content)
        self.content.append(Bookmark(index + 1, path))
        self._save_bookmarks()

    def _go_to_bookmark(self, bookmark: Bookmark) -> None:
        self._commands.change_dir(bookmark.text)
        self._commands.toggle_pane_view()

    def _handle_enter(self) -> None:
        self._go_to_bookmark(self.listbox.focus)

    def _handle_number(self, number: int) -> None:
        try:
            self._go_to_bookmark(self.content[number - 1])
        except:
            self._commands.error('no such bookmark: {}'.format(number))

    def _renumber_bookmarks(self) -> None:
        i = 1
        for b in self.content:
            b.index = i
            i += 1

    def _on_delete(self, entry: Bookmark) -> None:
        self._renumber_bookmarks()
        self._save_bookmarks()

    def _on_paste(self, entry: Bookmark) -> None:
        self._renumber_bookmarks()
        self._save_bookmarks()

