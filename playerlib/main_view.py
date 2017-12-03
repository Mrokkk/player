#!/usr/bin/env python3

import urwid
from playerlib.helpers.separators import *

class MainView(urwid.WidgetWrap):

    def __init__(self, file_browser, bookmarks, playlist, track_info):
        self._file_browser = file_browser
        self._bookmarks = bookmarks
        self._playlist = playlist
        self._track_info = track_info
        self._left_pane = urwid.WidgetPlaceholder(file_browser)
        self._right_pane = urwid.Frame(urwid.Pile([playlist]),
                footer=urwid.AttrWrap(urwid.Text('Playlist'), 'foot'))
        self.columns = urwid.Columns([
            ('weight', 48, self._left_pane),
            VerticalSeparator(),
            ('weight', 50, self._right_pane)
        ])
        self.columns.set_focus(0)
        super().__init__(self.columns)

    def keypress(self, size, key):
        if key == 'right' or key == 'left': return key
        return super().keypress(size, key)

    def handle_input(self, key):
        if self.columns.focus == self._left_pane:
            return self.columns.focus.original_widget.handle_input(key)
        else:
            return self._playlist.handle_input(key)

    def switch_panes(self):
        self.columns.set_focus(0 if self.columns.focus_position else 2)

    def _toggle_left_pane(self):
        if self.columns.focus.original_widget == self._file_browser:
            self.columns.focus.original_widget = self._bookmarks
        else:
            self.columns.focus.original_widget = self._file_browser

    def _toggle_right_pane(self):
        if len(self._right_pane.contents['body'][0].contents) == 3:
            self._right_pane.contents['body'] = (urwid.Pile([self._playlist]), None)
        else:
            self._right_pane.contents['body'] = (urwid.Pile([
                    self._playlist,
                    HorizontalSeparator(),
                    self._track_info]), None)

    def toggle_pane_view(self):
        if self.columns.focus == self._left_pane:
            self._toggle_left_pane()
        else:
            self._toggle_right_pane()

    def switch_left(self):
        self.columns.set_focus(0)

    def switch_right(self):
        self.columns.set_focus(2)

    @property
    def focus(self):
        if self.columns.focus == self._left_pane:
            return self.columns.focus.original_widget
        else:
            return self._playlist

