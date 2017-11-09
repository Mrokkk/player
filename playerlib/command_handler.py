#!/usr/bin/env python3

class CommandHandler:

    class Mode:
        COMMAND = 1
        SEARCH_FORWARD = 2
        SEARCH_BACKWARD = 3

    def __init__(self, context):
        self.context = context
        self.mode_map = {
            self.Mode.COMMAND: self._command_mode,
            self.Mode.SEARCH_FORWARD: self._search_forward_mode,
            self.Mode.SEARCH_BACKWARD: self._search_backward_mode
        }
        self.player_commands = [
            'quit',
        ]
        self.playlist_commands = [
            'add_to_playlist',
        ]
        self.playback_commands = [
            'pause', 'stop', 'next', 'prev', 'seek'
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
        module = None
        if command in self.player_commands:
            module = 'self.context.player_controller'
        elif command in self.playback_commands:
            module = 'self.context.playback_controller'
        elif command in self.playlist_commands:
            module = 'self.context.playlist'
        elif command in self.view_commands:
            module = 'self.context.view'
        if module == None:
            raise RuntimeError('no such command: ' + command)
        eval('{}.{}({})'.format(module, command,
            '' if not len(args) else '\'{}\''.format(args[0]))) # FIXME

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

