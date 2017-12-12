#!/usr/bin/env python3

import urwid
from .vertical_box import *

class Window(urwid.WidgetWrap):

    def __init__(self, main_view, command_panel):
        self.main_view = main_view if main_view else urwid.ListBox([])
        self.command_panel = command_panel
        self.view = urwid.WidgetPlaceholder(self.main_view)
        super().__init__(urwid.Frame(self.view, footer=self.command_panel))

    def keypress(self, size, key):
        if key in self.command_panel.activation_keys and not self.command_panel.is_active():
            self._focus_command_panel()
            self.command_panel.activate(key)
            return None
        return super().keypress(size, key)

    def handle_input(self, key):
        if self._w.focus_position == 'footer':
            return self.command_panel.handle_input(key, self._focus_body)
        self.main_view.handle_input(key)

    def switch_panes(self):
        self.main_view.switch_panes()

    def toggle_pane_view(self):
        self.main_view.toggle_pane_view()

    def _focus_command_panel(self):
        self._w.focus_position = 'footer'

    def _focus_body(self):
        self._w.focus_position = 'body'

    @property
    def focus(self):
        if isinstance(self.main_view, VerticalBox):
            return self.main_view.focus
        else: return self.main_view
