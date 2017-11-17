#!/usr/bin/env python3

class CommandHandler:

    class Mode:
        COMMAND = 1
        SEARCH_FORWARD = 2
        SEARCH_BACKWARD = 3


    class Commands:
        def __init__(self, context):
            self._context = context

        def quit(self):
            self._context.quit()

        def add_to_playlist(self, path):
            self._context.playlist.add_to_playlist(path)

        def save_playlist(self, playlist_file):
            self._context.playlist.save_playlist(playlist_file)

        def load_playlist(self, playlist_file):
            self._context.playlist.load_playlist(playlist_file)

        def pause(self):
            self._context.playback_controller.pause()

        def stop(self):
            self._context.playback_controller.stop()

        def next(self):
            self._context.playback_controller.next()

        def prev(self):
            self._context.playback_controller.prev()

        def seek(self, value):
            self._context.playback_controller.seek(value)

        def switch_panes(self):
            self._context.view.switch_panes()

        def set(self, key, value):
            if key == 'volume':
                self._context.playback_controller.set_volume(value)
            else:
                raise RuntimeError('No such key: {}'.format(key))


    def __init__(self, context):
        self.context = context
        self.mode_map = {
            self.Mode.COMMAND: self._command_mode,
            self.Mode.SEARCH_FORWARD: self._search_forward_mode,
            self.Mode.SEARCH_BACKWARD: self._search_backward_mode
        }
        self.command_mapping = {
            'q': 'quit',
            'qa': 'quit',
            'e': 'add_to_playlist',
        }
        self.commands = self.Commands(context)

    def _format_arguments(self, args):
        if len(args) == 0: return ''
        return ','.join('\'{}\''.format(arg.strip()) for arg in args)

    def _command_mode(self, command):
        splitted = command.split()
        command = splitted[0]
        args = splitted[1:]
        if command in self.command_mapping:
            command = self.command_mapping[command]
        if not hasattr(self.commands, command):
            raise RuntimeError('no such command: ' + command)
        eval('self.commands.{}({})'.format(command, self._format_arguments(args)))

    def _search_forward_mode(self, command):
        self.context.view.focus.search_forward(command)

    def _search_backward_mode(self, command):
        self.context.view.focus.search_backward(command)

    def list_commands(self):
        import inspect
        commands = [x[0] for x in inspect.getmembers(self.commands, predicate=inspect.ismethod)]
        commands.extend(self.command_mapping.keys())
        return commands

    def execute(self, command):
        if not command: return
        if command.startswith(':'):
            mode = self.Mode.COMMAND
        elif command.startswith('/'):
            mode = self.Mode.SEARCH_FORWARD
        elif command.startswith('?'):
            mode = self.Mode.SEARCH_BACKWARD
        self.mode_map[mode](command[1:])

