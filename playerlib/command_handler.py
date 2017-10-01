#!/usr/bin/env python3

class CommandHandler:

    class Mode:
        COMMAND = 1
        SEARCH_FORWARD = 2
        SEARCH_BACKWARD = 3

    def __init__(self, context):
        self.context = context
        self.player_controller = context.player_controller
        self.mode_map = {
            self.Mode.COMMAND: self._command_mode,
            self.Mode.SEARCH_FORWARD: self._search_forward_mode,
            self.Mode.SEARCH_BACKWARD: self._search_backward_mode
        }
        self.player_commands = [
            'add_to_playlist', 'pause', 'stop', 'next', 'prev', 'quit',
        ]
        self.view_commands = [
            'switch_panes',
        ]
        self.command_mapping = {
            'q': 'quit',
            'qa': 'quit',
            'e': 'add_to_playlist',
        }

    def _command_mode(self, command):
        splitted = command.split()
        command = splitted[0]
        args = splitted[1:]
        if command in self.command_mapping:
            command = self.command_mapping[command]
        if command in self.player_commands:
            eval('self.player_controller.{}({})'.format(
                command,
                '' if not len(args) else '\'{}\''.format(args[0]))) # FIXME
        elif command in self.view_commands:
            eval('self.context.view.{}({})'.format(
                command,
                '' if not len(args) else '\'{}\''.format(args[0]))) # FIXME
        else:
            raise RuntimeError('no such command: ' + command)

    def _search_forward_mode(self, command):
        self.context.view.focus.search_forward(command)

    def _search_backward_mode(self, command):
        self.context.view.focus.search_backward(command)

    def execute(self, command):
        if not command: return
        if command.startswith(':'):
            mode = self.Mode.COMMAND
        elif command.startswith('/'):
            mode = self.Mode.SEARCH_FORWARD
        elif command.startswith('?'):
            mode = self.Mode.SEARCH_BACKWARD
        self.mode_map[mode](command[1:])

