#!/usr/bin/env python3

import os
import sys
import urwid
import asyncio

class FileBrowser:

    class DirEntry(urwid.Button):

        def __init__(self, name, is_a_dir=False, callback=None):
            super().__init__(name, on_press=callback)
            self.name = name
            if is_a_dir:
                self._w = urwid.AttrMap(urwid.SelectableIcon([u'▸ ', name, '/'], 0), 'dir', 'dir_focused')
            else:
                self._w = urwid.AttrMap(urwid.SelectableIcon(['  ', name], 0), 'file', 'file_focused')

        def __lt__(self, other):
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
        self.load_dir(os.getcwd())

    def load_dir(self, dirname):
        self.dir_name = dirname
        self.dir_list = sorted([self.DirEntry(a, os.path.isdir(a), callback=self.callback) for a in os.listdir(self.dir_name)])
        self.content = urwid.SimpleListWalker(self.dir_list)
        self.listbox = urwid.ListBox(self.content)
        self.header = urwid.Text(self.dir_name)
        self.footer = urwid.AttrWrap(urwid.Text(self.footer_text), 'foot')
        self.view = urwid.Frame(
            urwid.AttrWrap(self.listbox, 'body'),
            header=urwid.AttrWrap(self.header, 'head'),
            footer=self.footer)

    def _change_dir(self, dirname):
        self.dir_name = dirname
        self.header.set_text(dirname)
        self.dir_list = [self.DirEntry(a, is_a_dir=os.path.isdir(os.path.join(self.dir_name, a)),
            callback=self.callback) for a in os.listdir(self.dir_name)]
        self.content[:] = self.dir_list

    def callback(self, widget):
        self._change_dir(os.path.abspath(os.path.join(self.dir_name, widget.label)))

    def main(self):
        screen = urwid.raw_display.Screen()
        screen.set_terminal_properties(256)
        self.loop = urwid.MainLoop(self.view, self.palette,
            unhandled_input=self.unhandled_input,
            event_loop=urwid.AsyncioEventLoop(loop=asyncio.get_event_loop()),
            screen=screen)
        self.loop.run()

    def unhandled_input(self, key):
        if key in ('q','Q'):
            raise urwid.ExitMainLoop()

def main():
    FileBrowser().main()

if __name__ == '__main__':
    main()

