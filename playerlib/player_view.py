#!/usr/bin/env python3

import urwid
from playerlib.main_view import *

class PlayerView(urwid.WidgetWrap):

    def __init__(self, file_browser, bookmarks, playlist, command_panel):
        self.command_panel = command_panel
        self.main_view = MainView(file_browser, bookmarks, playlist)
        self.alternate_view = None
        self.view = urwid.WidgetPlaceholder(self.main_view)
        super().__init__(urwid.Frame(self.view, footer=self.command_panel))

    def unhandled_input(self, key):
        if self._w.focus_position == 'footer':
            return self.command_panel.unhandled_input(key)
        return self.main_view.unhandled_input(key)

    def switch_panes(self):
        self.main_view.switch_panes()

    def toggle_pane_view(self):
        self.main_view.toggle_pane_view()

    def focus_command_panel(self):
        self._w.focus_position = 'footer'

    def focus_body(self):
        self._w.focus_position = 'body'

    @property
    def focus(self):
        return self.main_view.focus

