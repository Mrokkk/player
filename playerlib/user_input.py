#!/usr/bin/env python3

import logging
import re
import urwid

class InputStateMachine:

    def __init__(self, context):
        self.context = context
        self.keys = {
            'gg': lambda: self.context.view.focus.searchable_list().scroll_beginning(),
            'G': lambda: self.context.view.focus.searchable_list().scroll_end(),
            'dd': lambda: self.context.view.focus.searchable_list().delete(),
            'h': lambda: self.context.command_handler(':seek -10'),
            'l': lambda: self.context.command_handler(':seek +10'),
            'H': lambda: self.context.command_handler(':seek -60'),
            'L': lambda: self.context.command_handler(':seek +60'),
            ' ': lambda: self.context.command_handler(':pause'),
            '<C-w>left': lambda: self.context.view.main_view.switch_left(),
            '<C-w>right': lambda: self.context.view.main_view.switch_right(),
            '<C-w><C-w>': lambda: self.context.command_handler(':switch_panes'),
            '[': lambda: self.context.command_handler(':set volume -10'),
            ']': lambda: self.context.command_handler(':set volume +10'),
            'b': lambda: self.context.command_handler(':toggle_pane_view'),
        }
        self.state = ''
        self.alarm = None

    def _clear(self):
        if self.alarm: self.context.event_loop.remove_alarm(self.alarm)
        self.state = ''

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
        self.state = ''.join([self.state, key])
        for k in self.keys:
            if self.state == k:
                self.keys[self.state]()
                self._clear()
                return True
            elif k.startswith(self.state):
                self.alarm = self.context.event_loop.alarm(1, self._clear)
                return True
        self._clear()
        return False


class UserInput:

    def __init__(self, context):
        self.view = context.view
        self.command_handler = context.command_handler
        self.command_panel = context.command_panel
        self.sm = InputStateMachine(context)

    def handle_input(self, key):
        if key in self.command_panel.activation_keys:
            self.view.focus_command_panel()
            self.command_panel.activate(key)
        else:
            try:
                if not isinstance(key, tuple):
                    if self.sm.handle_key(key): return
                if not self.view.unhandled_input(key):
                    self.view.focus_body()
            except urwid.ExitMainLoop:
                raise
            except Exception as e:
                self.command_panel.error(str(e))

