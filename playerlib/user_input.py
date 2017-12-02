#!/usr/bin/env python3

import logging
import re
import urwid

class InputStateMachine:

    def __init__(self, context):
        self._context = context
        self._keys = {
            'gg': lambda: self._context.window.focus.searchable_list().scroll_beginning(),
            'G': lambda: self._context.window.focus.searchable_list().scroll_end(),
            'dd': lambda: self._context.window.focus.searchable_list().delete(),
            'h': lambda: self._context.command_handler(':seek -10'),
            'l': lambda: self._context.command_handler(':seek +10'),
            'H': lambda: self._context.command_handler(':seek -60'),
            'L': lambda: self._context.command_handler(':seek +60'),
            ' ': lambda: self._context.command_handler(':pause'),
            '<C-w>left': lambda: self._context.window.main_view.switch_left(),
            '<C-w>right': lambda: self._context.window.main_view.switch_right(),
            '<C-w><C-w>': lambda: self._context.command_handler(':switch_panes'),
            '[': lambda: self._context.command_handler(':set volume -10'),
            ']': lambda: self._context.command_handler(':set volume +10'),
            'b': lambda: self._context.command_handler(':toggle_pane_view'),
        }
        self._state = ''
        self._alarm = None

    def _clear(self):
        if self._alarm: self._context.event_loop.remove_alarm(self._alarm)
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
                self._alarm = self._context.event_loop.alarm(1, self._clear)
                return True
        self._clear()
        return False


class UserInput:

    def __init__(self, context):
        self.window = context.window
        self.command_handler = context.command_handler
        self.sm = InputStateMachine(context)

    def handle_input(self, key):
        try:
            if not isinstance(key, tuple):
                if self.sm.handle_key(key): return
            if not self.window.unhandled_input(key):
                self.window.focus_body()
        except urwid.ExitMainLoop:
            raise
        except Exception as e:
            self.command_handler(':error \"{}\"'.format(str(e)))

