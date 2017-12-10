#!/usr/bin/env python3

import logging
import re
import urwid
import playerlib.helpers.app

class InputStateMachine:

    def __init__(self, keys_mapping):
        self._keys = {
            'gg': lambda: playerlib.helpers.app.App().window.focus.searchable_list().scroll_beginning(),
            'G': lambda: playerlib.helpers.app.App().window.focus.searchable_list().scroll_end(),
            'dd': lambda: playerlib.helpers.app.App().window.focus.searchable_list().delete(),
            '<C-w>left': lambda: playerlib.helpers.app.App().window.main_view.switch_left(),
            '<C-w>right': lambda: playerlib.helpers.app.App().window.main_view.switch_right(),
            '<C-w><C-w>': lambda: playerlib.helpers.app.App().window.switch_panes(),
            'b': lambda: playerlib.helpers.app.App().window.toggle_pane_view(),
        }
        for k, v in keys_mapping.items():
            self._keys[k] = lambda v=v: playerlib.helpers.app.App().command_handler(v)
        self._state = ''
        self._alarm = None

    def _clear(self):
        if self._alarm: playerlib.helpers.app.App().loop.remove_alarm(self._alarm)
        self._state = ''
        self._alarm = None

    def _convert_key(self, key):
        if 'meta' in key:
            return re.sub(r'meta (.)', r'<M-\1>', key)
        elif 'ctrl' in key:
            return re.sub(r'ctrl (.)', r'<C-\1>', key)
        return key

    def handle_key(self, key):
        key = self._convert_key(key)
        if key == 'esc':
            self._clear()
            return False
        self._state = ''.join([self._state, key])
        for k in self._keys:
            if self._state == k:
                self._keys[self._state]()
                self._clear()
                return True
            elif k.startswith(self._state):
                self._alarm = playerlib.helpers.app.App().loop.alarm(1, self._clear)
                return True
        self._clear()
        return False


class UserInput:

    def __init__(self, keys_mapping):
        self.sm = InputStateMachine(keys_mapping)

    def handle_input(self, key):
        try:
            if not isinstance(key, tuple):
                if self.sm.handle_key(key): return
            playerlib.helpers.app.App().window.handle_input(key)
        except urwid.ExitMainLoop:
            raise
        except Exception as e:
            playerlib.helpers.app.App().command_panel.error(str(e))

