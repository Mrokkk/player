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


def create_screen():
    screen = urwid.raw_display.Screen()
    try:
        screen.set_terminal_properties(256)
    except:
        pass
    return screen


def handle_input(view, key):
    if key == ':':
        view.focus_position = 'footer'
        view.contents['footer'][0].set_caption(':')
        return
    if view.get_focus() == 'footer':
        if key == 'enter':
            if view.contents['footer'][0].get_edit_text().strip() == 'q':
                raise urwid.ExitMainLoop()
            view.contents['footer'][0].set_caption('')
            view.contents['footer'][0].set_edit_text('')
            view.focus_position = 'body'
    else:
        path = view.contents['body'][0].focus.unhandled_input(key)
        if path:
            view.contents['body'][0].contents[1][0].add(path)


def main():
    screen = create_screen()

    top = HorizontalBoxes()
    file_browser = FileBrowser()
    playlist = Playlist()
    top.open_box(file_browser)
    top.open_box(playlist)
    top.set_focus(0) # Set focus to file browser
    cli_panel = urwid.Edit()
    view = urwid.Frame(top, footer=cli_panel)

    urwid.MainLoop(
        view,
        config.color_palette,
        unhandled_input=lambda key: handle_input(view, key),
        event_loop=urwid.AsyncioEventLoop(loop=asyncio.get_event_loop()),
        screen=screen
    ).run()


if __name__ == '__main__':
    main()

