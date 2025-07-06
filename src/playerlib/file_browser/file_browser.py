#!/usr/bin/env python3

import logging
import os
import urwim

from .dir_entry import *

class FileBrowser(urwim.ViewWidget):

    footer_text:   str = 'Browser'
    dir_name:      str
    header:        urwim.Header
    content:       urwim.SimpleListWalker
    listbox:       urwim.ListWidget
    last_position: int
    logger:        logging.Logger

    def __init__(self, commands) -> None:
        self._commands = commands
        self.dir_name = os.getcwd()
        self.header = urwim.Header(self.dir_name)
        self.content = urwim.SimpleListWalker([])
        self.content.extend(self._read_dir(self.dir_name))
        self.listbox = urwim.ListWidget(self.content, readonly=True)
        self.last_position = 0
        self.logger = logging.getLogger('FileBrowser')
        callbacks = {
            'u': self._go_back,
            'enter': lambda: self._toggle_dir(self.content.get_focus()[0]),
            'R': lambda: self.change_dir('.'),
            'C': self._enter_selected_dir,
            'a': lambda: self._commands.add_to_playlist(self.content.get_focus()[0].path),
            'r': lambda: self._commands.replace_playlist(self.content.get_focus()[0].path),
            'B': lambda: self._commands.add_bookmark(self.dir_name),
        }
        super().__init__(self.listbox,
            'File browser',
            callbacks=callbacks,
            header=self.header)

    def current_dir(self) -> str:
        return self.dir_name

    def change_dir(self, dirname: str) -> None:
        path = os.path.abspath(os.path.join(self.dir_name, dirname))
        if not os.path.isdir(path): raise RuntimeError('Not a dir: {}'.format(path))
        self.dir_name = path
        self.content[0:] = self._read_dir(self.dir_name)
        self.header.text = path

    def _read_dir(self, path: str, level: int = 0) -> list[DirEntry]:
        return sorted([
            DirEntry(
                dir_entry,
                path,
                is_a_dir=os.path.isdir(os.path.join(path, dir_entry)),
                level=level
            ) for dir_entry in os.listdir(path) if not dir_entry.startswith('.')])

    def _show_dir(self, parent: DirEntry) -> None:
        parent_path = parent.path
        if not os.path.isdir(parent_path):
            return
        index = self.listbox.focus_position + 1
        dir_entries = self._read_dir(parent_path, parent.level + 1)
        if len(dir_entries):
            self.content[index:index] = dir_entries
            parent.open = True

    def _hide_dir(self, parent: DirEntry):
        index = self.listbox.focus_position + 1
        while True:
            del self.content[index]
            try:
                if self.content[index].level < parent.level + 1:
                    break
            except:
                break
        parent.open = False

    @urwim.asynchronous
    def _toggle_dir(self, parent: DirEntry) -> None:
        if parent.open:
            self._hide_dir(parent)
        else:
            self._show_dir(parent)

    def _enter_selected_dir(self) -> None:
        self.last_position = self.listbox.focus_position
        path = self.content.get_focus()[0].path
        self.change_dir(path)
        try:
            self.listbox.focus_position = 0
        except:
            pass

    def _go_back(self) -> None:
        self.change_dir('..')
        if self.last_position:
            self.listbox.focus_position = self.last_position
            self.last_position = 0

