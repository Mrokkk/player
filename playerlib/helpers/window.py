#!/usr/bin/env python3

import urwid

class Window(urwid.WidgetWrap):

    def __init__(self, main_view, command_panel):
        self.main_view = main_view
        self.command_panel = command_panel
        self.view = urwid.WidgetPlaceholder(self.main_view)
        super().__init__(urwid.Frame(self.view, footer=self.command_panel))

    def keypress(self, size, key):
        if key in self.command_panel.activation_keys:
            self._focus_command_panel()
            self.command_panel.activate(key)
            return None
        return super().keypress(size, key)

    def handle_input(self, key):
        if self._w.focus_position == 'footer':
            return self.command_panel.handle_input(key)
        return self.main_view.handle_input(key)

    def switch_panes(self):
        self.main_view.switch_panes()

    def toggle_pane_view(self):
        self.main_view.toggle_pane_view()

    def _focus_command_panel(self):
        self._w.focus_position = 'footer'

    def focus_body(self):
        self._w.focus_position = 'body'

    @property
    def focus(self):
        return self.main_view.focus

