#!/usr/bin/env python3

import logging
import os
import urwid

from playerlib.helpers.scrollable import *
from playerlib.helpers.helpers import *
from .dir_entry import *

class Header(urwid.WidgetWrap):
    def __init__(self, name):
        self._name = name
        super().__init__(urwid.AttrWrap(urwid.Text(self._name), 'head'))

    def set_text(self, text):
        self._name = text
        self._w.set_text(text)

    def text(self):
        return self._name


class Bookmarks(urwid.WidgetWrap):

    footer_text = 'Bookmarks'

    class Bookmark(urwid.Button):
        def __init__(self, index, path):
            self.index = index
            self._path = path
            self._w = urwid.AttrMap(urwid.SelectableIcon([str(index), ' ', self._path], 0),
                'file', 'file_focused')

        def keypress(self, size, key):
            return key

        def path(self):
            return self._path


    def __init__(self):
        self.header = Header('Bookmarks')
        self.content = urwid.SimpleListWalker([])
        self.content.append(self.header)
        self._load_bookmarks()
        self.listbox = urwid.ListBox(self.content)
        super().__init__(urwid.Frame(self.listbox, footer=urwid.AttrWrap(urwid.Text(self.footer_text), 'foot')))

    def __del__(self):
        self._save_bookmarks()

    def _save_bookmarks(self):
        import json
        path = os.path.join(os.path.expanduser('~'), '.config', 'player', 'bookmarks.json')
        try:
            with open(path, 'w') as f:
                json.dump([b.path() for b in self.content if b.__class__ == self.Bookmark], f)
        except: pass

    def _load_bookmarks(self):
        import json
        path = os.path.join(os.path.expanduser('~'), '.config', 'player', 'bookmarks.json')
        if os.path.exists(path):
            with open(path, 'r') as f:
                bookmarks = json.load(f)
                for i, b in enumerate(bookmarks):
                    self.content.append(self.Bookmark(i + 1, b))

    def __getitem__(self, index):
        if not index: return None
        return self.content[index].path()

    @property
    def focused(self):
        return self.listbox.focus.path()

    def add(self, path):
        index = len(self.content)
        self.content.append(self.Bookmark(index, path))
        self._save_bookmarks()


class FileBrowser(urwid.WidgetWrap):

    footer_text = 'Browser'

    def __init__(self, add_callback, error_handler):
        self.callback = add_callback
        self.error_handler = error_handler
        self.dir_name = os.getcwd()
        self.bookmarks = []
        self.header = Header(self.dir_name)
        self.dir_list = self._read_dir(self.dir_name)
        self.content = urwid.SimpleListWalker([])
        self.content.append(self.header)
        self.content.extend(self.dir_list)
        self.listbox = urwid.ListBox(self.content)
        self.last_position = 0
        self.logger = logging.getLogger('FileBrowser')
        self.file_browser_view = urwid.Frame(self.listbox,
            footer=urwid.AttrWrap(urwid.Text(self.footer_text), 'foot'))
        self.bookmarks_view = Bookmarks()
        self.view = urwid.WidgetPlaceholder(self.file_browser_view)
        super().__init__(self.view)

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
        self.content[1:] = self.dir_list

    def _show_dir(self, parent):
        parent_path = parent.path()
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

    def search_backward(self, pattern):
        index = self.listbox.focus_position - 1
        while True:
            try:
                if pattern in self.content[index].name:
                    self.listbox.focus_position = index
                    return
                index -= 1
                if index < 0: return
            except:
                break

    def _reload(self):
        self._change_dir('.')

    def _enter_selected_dir(self):
        self.last_position = self.listbox.focus_position
        self._change_dir(self.content.get_focus()[0].label)
        try:
            self.listbox.focus_position = 1
        except: pass

    def _go_back(self):
        self._change_dir('..')
        if self.last_position:
            self.listbox.focus_position = self.last_position
            self.last_position = 0

    def _replace_playlist(self):
        try:
            self.callback(self.content.get_focus()[0].path(), clear=True)
        except Exception as e:
            self.error_handler(str(e))

    def _add_to_playlist(self):
        try:
            # self.context.async_caller.call(lambda: self.context.command_handler.commands.add_to_playlist(self.content.get_focus()[0].path()))
            self.callback(self.content.get_focus()[0].path())
        except Exception as e:
            self.error_handler(str(e))

    def _switch_views(self):
        if self.view.original_widget == self.file_browser_view:
            self.view.original_widget = self.bookmarks_view
        else:
            self.view.original_widget = self.file_browser_view

    def _add_bookmark(self):
        self.bookmarks_view.add(self.dir_name)

    def _handle_bookmarks(self, key):
        try_to_scroll(self.listbox, key)
        if key == 'b':
            self._switch_views()
        elif key == 'enter':
            self._change_dir(self.bookmarks_view.focused)
            self._switch_views()
        else:
            try:
                index = int(key)
                self._change_dir(self.bookmarks_view[index])
                self._switch_views()
            except: log_exception(self.logger)

    def _handle_file_browser_view(self, key):
        try_to_scroll(self.listbox, key)
        if key == 'u':
            self._go_back()
        elif key == 'enter':
            self._toggle_dir(self.content.get_focus()[0])
        elif key == 'a':
            self._add_to_playlist()
        elif key == 'r':
            self._replace_playlist()
        elif key == 'R':
            self._reload()
        elif key == 'C':
            self._enter_selected_dir()
        elif key == 'b':
            self._switch_views()
        elif key == 'B':
            self._add_bookmark()
        elif key == 'home':
            self.listbox.focus_position = 0
        elif key == 'end':
            self.listbox.focus_position = len(self.content) - 1

    def unhandled_input(self, key):
        if self.view.original_widget == self.file_browser_view:
            return self._handle_file_browser_view(key)
        else:
            return self._handle_bookmarks(key)
