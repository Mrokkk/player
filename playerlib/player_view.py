#!/usr/bin/env python3

import urwid

class PlayerView(urwid.WidgetWrap):

    def __init__(self, file_browser, playlist, command_panel):
        self.columns = urwid.Columns([], dividechars=1)
        self.columns.contents.append((file_browser, self.columns.options('weight', 50)))
        self.columns.contents.append((playlist, self.columns.options('weight', 50)))
        self.columns.set_focus(0)
        self.command_panel = command_panel
        super().__init__(urwid.Frame(self.columns, footer=self.command_panel))

    def keypress(self, size, key):
        return self._w.keypress(size, key)

    def unhandled_input(self, key):
        if self._w.focus_position == 'footer':
            return self.command_panel.unhandled_input(key)
        return self.columns.focus.unhandled_input(key)

    def switch_panes(self):
        self.columns.set_focus(0 if self.columns.focus_position else 1)

    def focus_command_panel(self):
        self._w.focus_position = 'footer'

    def focus_body(self):
        self._w.focus_position = 'body'

    @property
    def focus(self):
        return self.columns.focus

    @property
    def focus_position(self):
        return self._w.focus_position

