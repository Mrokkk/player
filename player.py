#!/usr/bin/env python3

import os
import sys
import urwid
import asyncio

import config

class Playlist(urwid.WidgetWrap):

    class Entry(urwid.Button):

        def __init__(self, path):
            self.path = path
            self.name = os.path.basename(path)
            super().__init__(self.name)
            self._w = urwid.AttrMap(urwid.SelectableIcon(['  ', self.name], 0),
                'file', 'file_focused')

        def keypress(self, size, key):
            return key

    def __init__(self):
        self.list = []
        self.content = urwid.SimpleListWalker([])
        self.listbox = urwid.ListBox(self.content)
        self.header = urwid.AttrWrap(urwid.Text('Unnamed playlist'), 'head')
        self.footer = urwid.AttrWrap(urwid.Text('Playlist'), 'foot')
        super().__init__(urwid.Frame(
            self.listbox,
            header=self.header,
            footer=self.footer))

    def unhandled_input(self, key):
        pass

    def add(self, path):
        self.content.append(self.Entry(path))


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

    def __init__(self):
        self.dir_name = os.getcwd()
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
            return self.content.get_focus()[0].path()


class HorizontalBoxes(urwid.Columns):

    def __init__(self):
        super().__init__([], dividechars=1)

    def open_box(self, box):
        if self.contents:
            del self.contents[self.focus_position + 1:]
        self.contents.append((box, self.options('weight', 50)))
        self.focus_position = len(self.contents) - 1

    def keypress(self, size, key):
        if key == 'ctrl w':
            self.set_focus(0 if self.focus_position else 1)
            return None
        return self.focus.keypress(size, key)

class Player:

    def __init__(self):
        self.playlist = Playlist()
        self.file_browser = FileBrowser()
        self.cli_panel = urwid.Edit()
        self.top = HorizontalBoxes()
        self.top.open_box(self.file_browser)
        self.top.open_box(self.playlist)
        self.view = urwid.Frame(self.top, footer=self.cli_panel)
        self.screen = self._create_screen()
        self.main_loop = urwid.MainLoop(
            self.view,
            config.color_palette,
            unhandled_input=self._handle_input,
            event_loop=urwid.AsyncioEventLoop(loop=asyncio.get_event_loop()),
            screen=self.screen)

    def _handle_input(self, key):
        if key == ':':
            self.view.focus_position = 'footer'
            self.cli_panel.set_caption(':')
            return
        if self.view.get_focus() == 'footer':
            if key == 'enter':
                if self.cli_panel.get_edit_text().strip() == 'q':
                    raise urwid.ExitMainLoop()
                self.cli_panel.set_caption('')
                self.cli_panel.set_edit_text('')
                self.view.focus_position = 'body'
        else:
            path = self.top.focus.unhandled_input(key)
            if path:
                self.top.contents[1][0].add(path)

    def _create_screen(self):
        screen = urwid.raw_display.Screen()
        try:
            screen.set_terminal_properties(256)
        except:
            pass
        return screen

    def run(self):
        self.top.set_focus(0) # Set focus to file browser
        self.main_loop.run()


def main():
    Player().run()


if __name__ == '__main__':
    main()

