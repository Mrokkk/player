#!/usr/bin/env python3

import os
import urwid
import asyncio

import config
from file_browser import *
from horizontal_panes import *
from playlist import *

class Cli:

    def handle_command(self, command):
        if not command: return True
        if command == 'q' or command == 'qa':
            raise urwid.ExitMainLoop()
        else:
            raise RuntimeError('No such command: ' + command)


class CliPanel(urwid.Edit):

    def __init__(self, cli):
        super().__init__()
        self.cli = cli

    def unhandled_input(self, key):
        if key == 'enter':
            try:
                if self.cli.handle_command(self.get_edit_text().strip()):
                    self.set_caption('')
                    self.set_edit_text('')
            except RuntimeError as exc:
                self.set_edit_text('')
                self.set_caption(exc.__str__())


class Player:

    def __init__(self):
        self.playlist = Playlist()
        self.file_browser = FileBrowser()
        self.cli = Cli()
        self.cli_panel = CliPanel(self.cli)
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
        elif key == 'ctrl w':
            self.panes.switch_focus()
        else:
            path = self.view.focus.unhandled_input(key)
            if path:
                self.panes.contents[1][0].add(path)
            self.view.focus_position = 'body'

    def _create_screen(self):
        screen = urwid.raw_display.Screen()
        try:
            screen.set_terminal_properties(256)
        except:
            pass
        return screen

    def run(self):
        self.main_loop.run()

