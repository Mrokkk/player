#!/usr/bin/env python3

import os
import urwid

from .dir_entry import *

class FileBrowser(urwid.WidgetWrap):

    footer_text = 'Browser'

    def __init__(self, add_callback):
        self.dir_name = os.getcwd()
        self.callback = add_callback
        self.dir_list = self._read_dir(self.dir_name)
        self.content = urwid.SimpleListWalker(self.dir_list)
        self.listbox = urwid.ListBox(self.content)
        self.header = urwid.AttrWrap(urwid.Text(self.dir_name), 'head')
        self.footer = urwid.AttrWrap(urwid.Text(self.footer_text), 'foot')
        super().__init__(urwid.Frame(
            self.listbox,
            header=self.header,
            footer=self.footer))

    def _read_dir(self, path, level=0):
        return sorted([
            DirEntry(
                dir_entry,
                path,
                is_a_dir=os.path.isdir(os.path.join(path, dir_entry)),
                level=level
            ) for dir_entry in os.listdir(path) if not dir_entry.startswith('.')])

    def _change_dir(self, dirname):
        path = os.path.abspath(os.path.join(self.dir_name, dirname))
        if not os.path.isdir(path): return
        self.dir_name = path
        self.dir_list = self._read_dir(self.dir_name)
        self.header.set_text(path)
        self.content[:] = self.dir_list

    def _show_dir(self, parent):
        parent_path = parent.path()
        if not os.path.isdir(parent_path): return
        index = self.listbox.focus_position + 1
        self.content[index:index] = self._read_dir(parent_path, parent.level + 1)
        parent.open = True

    def _hide_dir(self, parent):
        # TODO
        pass

    def _toggle_dir(self, parent):
        if parent.open:
            self._hide_dir(parent)
        else:
            self._show_dir(parent)

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

