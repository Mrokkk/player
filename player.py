#!/usr/bin/env python3

import os
import urwid
import asyncio

import config
from file_browser import *
from horizontal_panes import *
from playlist import *

class Player:

    def __init__(self):
        self.playlist = Playlist()
        self.file_browser = FileBrowser()
        self.cli_panel = urwid.Edit()
        self.panes = HorizontalPanes([self.file_browser, self.playlist])
        self.view = urwid.Frame(self.panes, footer=self.cli_panel)
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
            path = self.panes.focus.unhandled_input(key)
            if path:
                self.panes.contents[1][0].add(path)

    def _create_screen(self):
        screen = urwid.raw_display.Screen()
        try:
            screen.set_terminal_properties(256)
        except:
            pass
        return screen

    def run(self):
        self.panes.set_focus(0) # Set focus to file browser
        self.main_loop.run()


def main():
    Player().run()


if __name__ == '__main__':
    main()

