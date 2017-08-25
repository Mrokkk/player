#!/usr/bin/env python3

import os
import sys
import urwid
import asyncio

class FileBrowser:

    class DirEntry(urwid.Button):

        signals = ['enter']

        def __init__(self, name, is_a_dir=False, callback=None):
            super().__init__(name)
            self.name = name
            self.isdir = is_a_dir
            if is_a_dir:
                self._w = urwid.AttrMap(urwid.SelectableIcon([u'▸ ', name, '/'], 0), 'dir', 'dir_focused')
            else:
                self._w = urwid.AttrMap(urwid.SelectableIcon(['  ', name], 0), 'file', 'file_focused')
            urwid.connect_signal(self, 'enter', callback)

        def _emit(self, signal):
            urwid.emit_signal(self, signal, self.label)

        def keypress(self, size, key):
            if key == 'enter':
                self._emit('enter')
            return key

        def __lt__(self, other):
            if self.isdir and not other.isdir: return True
            elif not self.isdir and other.isdir: return False
            return self.name.lower() < other.name.lower()

    palette = [
        ('body', '', '', ''),
        ('head', 'yellow', 'black', '', '#a30', ''),
        ('foot', 'light gray', 'black'),
        ('file', 'white', '', '', '#fff', ''),
        ('file_focused', 'white', 'black', '', '#fff', 'g11'),
        ('dir', 'dark green', '', '', '#8a5', ''),
        ('dir_focused', 'dark green', 'black', '', '#8a5', 'g11')
    ]

    footer_text = 'Browser'

    def __init__(self):
        self.dir_name = os.getcwd()
        self._read_dir()
        self.content = urwid.SimpleListWalker(self.dir_list)
        self.listbox = urwid.ListBox(self.content)
        self.header = urwid.Text(self.dir_name)
        self.footer = urwid.AttrWrap(urwid.Text(self.footer_text), 'foot')
        self.view = urwid.Frame(
            urwid.AttrWrap(self.listbox, 'body'),
            header=urwid.AttrWrap(self.header, 'head'),
            footer=self.footer)
        urwid.register_signal(FileBrowser, 'back')
        urwid.connect_signal(self, 'back', lambda: self._change_dir('..'))

    def _read_dir(self):
        self.dir_list = sorted([self.DirEntry(a, is_a_dir=os.path.isdir(os.path.join(self.dir_name, a)),
            callback=self._callback) for a in os.listdir(self.dir_name)])

    def _change_dir(self, dirname):
        path = os.path.abspath(os.path.join(self.dir_name, dirname))
        if not os.path.isdir(path): return
        self.dir_name = path
        self._read_dir()
        self.header.set_text(path)
        self.content[:] = self.dir_list

    def _callback(self, dirname):
        self._change_dir(dirname)

    def main(self):
        self.screen = urwid.raw_display.Screen()
        self.screen.set_terminal_properties(256)
        self.loop = urwid.MainLoop(
            self.view,
            self.palette,
            unhandled_input=self.unhandled_input,
            event_loop=urwid.AsyncioEventLoop(loop=asyncio.get_event_loop()),
            screen=self.screen)
        self.loop.run()

    def unhandled_input(self, key):
        if key in ('q','Q'):
            raise urwid.ExitMainLoop()
        if key == 'u':
            urwid.emit_signal(self, 'back')

def main():
    FileBrowser().main()

if __name__ == '__main__':
    main()

