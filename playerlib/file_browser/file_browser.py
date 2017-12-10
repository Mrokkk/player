#!/usr/bin/env python3

import logging
import os
import urwid

from playerlib.helpers.app import *
from playerlib.helpers.asynchronous import *
from playerlib.helpers.header import *
from playerlib.helpers.list_widget import *
from playerlib.helpers.listbox_entry import *
from playerlib.helpers.view_widget import *
from .dir_entry import *

class FileBrowser(ViewWidget):

    footer_text = 'Browser'

    def __init__(self):
        self.dir_name = os.getcwd()
        self.header = Header(self.dir_name)
        self.content = urwid.SimpleListWalker([])
        self.content.extend(self._read_dir(self.dir_name))
        self.listbox = ListWidget(self.content, readonly=True)
        self.last_position = 0
        self.logger = logging.getLogger('FileBrowser')
        callbacks = {
            'u': self._go_back,
            'enter': lambda: self._toggle_dir(self.content.get_focus()[0]),
            'R': lambda: self.change_dir('.'),
            'C': self._enter_selected_dir,
            'a': lambda: App().command_handler(':add_to_playlist \"{}\"'.format(self.content.get_focus()[0].path)),
            'r': lambda: App().command_handler(':replace_playlist \"{}\"'.format(self.content.get_focus()[0].path)),
            'B': lambda: App().command_handler(':add_bookmark \"{}\"'.format(self.dir_name)),
        }
        super().__init__(self.listbox,
            callbacks,
            'File browser',
            header=self.header)

    def change_dir(self, dirname):
        path = os.path.abspath(os.path.join(self.dir_name, dirname))
        if not os.path.isdir(path): raise RuntimeError('Not a dir: {}'.format(path))
        self.dir_name = path
        self.content[0:] = self._read_dir(self.dir_name)
        self.header.text = path

    def _read_dir(self, path, level=0):
        return sorted([
            DirEntry(
                dir_entry,
                path,
                is_a_dir=os.path.isdir(os.path.join(path, dir_entry)),
                level=level
            ) for dir_entry in os.listdir(path) if not dir_entry.startswith('.')])

    def _show_dir(self, parent):
        parent_path = parent.path
        if not os.path.isdir(parent_path): return
        index = self.listbox.focus_position + 1
        dir_entries = self._read_dir(parent_path, parent.level + 1)
        if len(dir_entries):
            self.content[index:index] = dir_entries
            parent.open = True

    def _hide_dir(self, parent):
        index = self.listbox.focus_position + 1
        while True:
            del self.content[index]
            try:
                if self.content[index].level < parent.level + 1: break
            except: break
        parent.open = False

    @asynchronous
    def _toggle_dir(self, parent):
        if parent.open:
            self._hide_dir(parent)
        else:
            self._show_dir(parent)

    def _enter_selected_dir(self):
        self.last_position = self.listbox.focus_position
        path = self.content.get_focus()[0].path
        self.change_dir(path)
        try:
            self.listbox.focus_position = 0
        except: pass

    def _go_back(self):
        self.change_dir('..')
        if self.last_position:
            self.listbox.focus_position = self.last_position
            self.last_position = 0

