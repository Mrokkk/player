#!/usr/bin/env python3

import os
import urwid

from .dir_entry import *

class FileBrowser(urwid.WidgetWrap):

    footer_text = 'Browser'

    def __init__(self, add_callback):
        self.dir_name = os.getcwd()
        self.callback = add_callback
        self._read_dir()
        self.content = urwid.SimpleListWalker(self.dir_list)
        self.listbox = urwid.ListBox(self.content)
        self.header = urwid.AttrWrap(urwid.Text(self.dir_name), 'head')
        self.footer = urwid.AttrWrap(urwid.Text(self.footer_text), 'foot')
        super().__init__(urwid.Frame(
            self.listbox,
            header=self.header,
            footer=self.footer))

    def _read_dir(self):
        self.dir_list = sorted([
            DirEntry(
                dir_entry,
                str(self.dir_name),
                is_a_dir=os.path.isdir(os.path.join(self.dir_name, dir_entry)),
            ) for dir_entry in os.listdir(self.dir_name) if not dir_entry.startswith('.')])

    def _change_dir(self, dirname):
        path = os.path.abspath(os.path.join(self.dir_name, dirname))
        if not os.path.isdir(path): return
        self.dir_name = path
        self._read_dir()
        self.header.set_text(path)
        self.content[:] = self.dir_list

    def _show_dir(self, item):
        if not os.path.isdir(item.path()): return
        index = self.listbox.focus_position + 1
        self.content[index:index] = sorted([
            DirEntry(
                d,
                item.path(),
                is_a_dir=os.path.isdir(os.path.join(item.path(), d)),
                level=item.level + 1
            ) for d in os.listdir(item.path()) if not d.startswith('.')])
        item.open = True

    def _hide_dir(self, item):
        # TODO
        pass

    def _toggle_dir(self, item):
        if item.open:
            self._hide_dir(item)
        else:
            self._show_dir(item)

    def unhandled_input(self, key):
        if key == 'u':
            self._change_dir('..')
        elif key == 'enter':
            self._toggle_dir(self.content.get_focus()[0])
        elif key == 'a':
            self.callback(self.content.get_focus()[0].path())
        elif key == 'r':
            self.callback(self.content.get_focus()[0].path(), True)
        elif key == 'C':
            self._change_dir(self.content.get_focus()[0].label)

