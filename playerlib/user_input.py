#!/usr/bin/env python3

class UserInput:

    def __init__(self, view, command_handler, command_panel):
        self.view = view
        self.command_handler = command_handler
        self.command_panel = command_panel
        self.key_to_command_mapping = {
            'h': ':seek -10',
            'l': ':seek +10',
            'H': ':seek -60',
            'L': ':seek +60',
            ' ': ':pause',
            'ctrl w': ':switch_panes',
            '[': ':set volume -10',
            ']': ':set volume +10',
            'b': ':toggle_pane_view',
        }

    def handle_input(self, key):
        if key in self.command_panel.activation_keys:
            self.view.focus_command_panel()
            self.command_panel.activate(key)
        else:
            if key in self.key_to_command_mapping:
                self.command_handler(self.key_to_command_mapping[key])
                return
            if not self.view.unhandled_input(key):
                self.view.focus_body()

