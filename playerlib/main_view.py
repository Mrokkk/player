#!/usr/bin/env python3

import urwid

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
                ('weight', 50, self._left_pane),
                ('weight', 50, self._right_pane)
            ],
            dividechars=1)
        self.columns.set_focus(0)
        super().__init__(self.columns)

    def unhandled_input(self, key):
        if self.columns.focus == self._left_pane:
            return self.columns.focus.original_widget.unhandled_input(key)
        else:
            return self._playlist.unhandled_input(key)

    def switch_panes(self):
        self.columns.set_focus(0 if self.columns.focus_position else 1)

    def toggle_pane_view(self):
        if self.columns.focus == self._left_pane:
            if self.columns.focus.original_widget == self._file_browser:
                self.columns.focus.original_widget = self._bookmarks
            else:
                self.columns.focus.original_widget = self._file_browser
        else:
            if len(self._right_pane.contents['body'][0].contents) == 2:
                self._right_pane.contents['body'] = (urwid.Pile([self._playlist]), None)
            else:
                self._right_pane.contents['body'] = (urwid.Pile([self._playlist, self._track_info]), None)

    @property
    def focus(self):
        if self.columns.focus == self._left_pane:
            return self.columns.focus.original_widget
        else:
            return self._playlist

