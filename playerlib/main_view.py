#!/usr/bin/env python3

import urwid

class MainView(urwid.WidgetWrap):

    def __init__(self, file_browser, bookmarks, playlist):
        self._file_browser = file_browser
        self._bookmarks = bookmarks
        self._playlist = playlist
        self._left_pane = urwid.WidgetPlaceholder(file_browser)
        self._right_pane = urwid.WidgetPlaceholder(playlist)
        self.columns = urwid.Columns([
                ('weight', 50, self._left_pane),
                ('weight', 50, self._right_pane)
            ],
            dividechars=1)
        self.columns.set_focus(0)
        super().__init__(self.columns)

    def unhandled_input(self, key):
        return self.columns.focus.original_widget.unhandled_input(key)

    def switch_panes(self):
        self.columns.set_focus(0 if self.columns.focus_position else 1)

    def toggle_pane_view(self):
        if self.columns.focus.original_widget == self._file_browser:
            self.columns.focus.original_widget = self._bookmarks
        else:
            self.columns.focus.original_widget = self._file_browser

    @property
    def focus(self):
        return self.columns.focus.original_widget

