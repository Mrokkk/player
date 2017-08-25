#!/usr/bin/env python3

import os
import sys
import urwid
import asyncio

import config

class FileBrowser:

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

        def __lt__(self, other):
            if self.isdir and not other.isdir: return True
            elif not self.isdir and other.isdir: return False
            return self.name.lower() < other.name.lower()

    def __init__(self):
        self.dir_name = os.getcwd()
        self._read_dir()
        self.content = urwid.SimpleListWalker(self.dir_list)
        self.listbox = urwid.ListBox(self.content)
        self.header = urwid.Text(self.dir_name)
        self.footer = urwid.AttrWrap(urwid.Text(self.footer_text), 'foot')
        self.view = urwid.Frame(
            self.listbox,
            header=urwid.AttrWrap(self.header, 'head'),
            footer=self.footer)
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

    def _unhandled_input(self, key):
        if key in ('q','Q'):
            raise urwid.ExitMainLoop()
        if key == 'u':
            urwid.emit_signal(self, 'exit_dir')

    def main(self):
        self.screen = urwid.raw_display.Screen()
        try:
            self.screen.set_terminal_properties(256)
        except:
            pass
        self.loop = urwid.MainLoop(
            self.view,
            config.color_palette,
            unhandled_input=self._unhandled_input,
            event_loop=urwid.AsyncioEventLoop(loop=asyncio.get_event_loop()),
            screen=self.screen)
        self.loop.run()

def main():
    FileBrowser().main()

if __name__ == '__main__':
    main()

