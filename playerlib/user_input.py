#!/usr/bin/env python3

class UserInput:

    def __init__(self, view, command_handler, command_panel):
        self.view = view
        self.command_handler = command_handler
        self.command_panel = command_panel
        self.error_handler = command_panel.error
        self.key_to_command_mapping = {
            'h': ':seek -10',
            'l': ':seek +10',
            'H': ':seek -60',
            'L': ':seek +60',
            ' ': ':pause',
            'ctrl w': ':switch_panes',
        }

    def handle_input(self, key):
        if key in self.command_panel.activation_keys:
            self.view.focus_command_panel()
            self.command_panel.activate(key)
        else:
            if key in self.key_to_command_mapping:
                try:
                    self.command_handler.execute(self.key_to_command_mapping[key])
                except Exception as e:
                    self.error_handler(str(e))
                return
            if not self.view.unhandled_input(key):
                self.view.focus_body()

