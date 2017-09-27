#!/usr/bin/env python3

import os
import urwid

from .dir_entry import *

class FileBrowser(urwid.WidgetWrap):

    footer_text = 'Browser'

    def __init__(self, add_callback, error_handler):
        self.callback = add_callback
        self.error_handler = error_handler
        self.dir_name = os.getcwd()
        self.dir_list = self._read_dir(self.dir_name)
        self.content = urwid.SimpleListWalker(self.dir_list)
        self.listbox = urwid.ListBox(self.content)
        self.header = urwid.AttrWrap(urwid.Text(self.dir_name), 'head')
        super().__init__(urwid.Frame(
            self.listbox,
            header=self.header,
            footer=urwid.AttrWrap(urwid.Text(self.footer_text), 'foot')))

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
        index = self.listbox.focus_position + 1
        while True:
            del self.content[index]
            if self.content[index].level < parent.level + 1: break
        parent.open = False

    def _toggle_dir(self, parent):
        if parent.open:
            self._hide_dir(parent)
        else:
            self._show_dir(parent)

    def search_forward(self, pattern):
        index = self.listbox.focus_position + 1
        while True:
            try:
                if pattern in self.content[index].name:
                    self.listbox.focus_position = index
                    return
                index += 1
            except:
                break

    def unhandled_input(self, key):
        if key == 'u':
            self._change_dir('..')
        elif key == 'enter':
            self._toggle_dir(self.content.get_focus()[0])
        elif key == 'a':
            try:
                self.callback(self.content.get_focus()[0].path())
            except Exception as e:
                self.error_handler(str(e))
        elif key == 'r':
            try:
                self.callback(self.content.get_focus()[0].path(), True)
            except Exception as e:
                self.error_handler(str(e))
        elif key == 'R':
            self._change_dir('.')
        elif key == 'C':
            self._change_dir(self.content.get_focus()[0].label)
        else:
            try:
                if key[0] == 'mouse press':
                    if key[1] == 5.0:
                        self.listbox.focus_position += 1
                    elif key[1] == 4.0:
                        self.listbox.focus_position -= 1
            except:
                pass

