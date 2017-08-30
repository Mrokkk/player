#!/usr/bin/env python3

import os
import urwid

import config

class FileBrowser(urwid.WidgetWrap):

    footer_text = 'Browser'

    class DirEntry(urwid.Button):

        signals = ['enter_dir']

        def __init__(self, name, parent_path, is_a_dir=False, callback=None):
            super().__init__(name)
            self.name = name
            self.parent_path = parent_path
            self.isdir = is_a_dir
            if is_a_dir:
                self._w = urwid.AttrMap(urwid.SelectableIcon([u'▸ ', name, '/'], 0),
                    'dir', 'dir_focused')
            else:
                self._w = urwid.AttrMap(urwid.SelectableIcon(['  ', name], 0),
                    'file', 'file_focused')
            urwid.connect_signal(self, 'enter_dir', callback)

        def _emit(self, signal):
            urwid.emit_signal(self, signal, self.label)

        def keypress(self, size, key):
            if key == 'C':
                self._emit('enter_dir')
            return key

        def path(self):
            return os.path.join(self.parent_path, self.name)

        def __lt__(self, other):
            if self.isdir and not other.isdir: return True
            elif not self.isdir and other.isdir: return False
            return self.name.lower() < other.name.lower()

    def __init__(self, enter_callback):
        self.dir_name = os.getcwd()
        self.callback = enter_callback
        self._read_dir()
        self.content = urwid.SimpleListWalker(self.dir_list)
        self.listbox = urwid.ListBox(self.content)
        self.header = urwid.AttrWrap(urwid.Text(self.dir_name), 'head')
        self.footer = urwid.AttrWrap(urwid.Text(self.footer_text), 'foot')
        super().__init__(urwid.Frame(
            self.listbox,
            header=self.header,
            footer=self.footer))
        urwid.register_signal(FileBrowser, 'exit_dir')
        urwid.connect_signal(self, 'exit_dir', lambda: self._change_dir('..'))

    def _callback(self, dirname):
        self._change_dir(dirname)

    def _read_dir(self):
        self.dir_list = sorted([
            self.DirEntry(
                dir_entry,
                str(self.dir_name),
                is_a_dir=os.path.isdir(os.path.join(self.dir_name, dir_entry)),
                callback=self._callback
            ) for dir_entry in os.listdir(self.dir_name)])

    def _change_dir(self, dirname):
        path = os.path.abspath(os.path.join(self.dir_name, dirname))
        if not os.path.isdir(path): return
        self.dir_name = path
        self._read_dir()
        self.header.set_text(path)
        self.content[:] = self.dir_list

    def unhandled_input(self, key):
        if key == 'u':
            urwid.emit_signal(self, 'exit_dir')
        if key == 'enter':
            self.callback(self.content.get_focus()[0].path())

