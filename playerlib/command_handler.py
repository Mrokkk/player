#!/usr/bin/env python3

import logging
import shlex
from playerlib.async import *

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

        @async
        def add_to_playlist(self, path):
            try:
                self._context.playlist.add_to_playlist(path)
            except Exception as e:
                self.error(str(e))

        def clear_playlist(self):
            self._context.playlist.clear()

        @async
        def save_playlist(self, playlist_file):
            try:
                self._context.playlist.save_playlist(playlist_file)
            except Exception as e:
                self.error(str(e))

        @async
        def load_playlist(self, playlist_file):
            try:
                self._context.playlist.load_playlist(playlist_file)
            except Exception as e:
                self.error(str(e))

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

        def toggle_pane_view(self):
            self._context.view.toggle_pane_view()

        def add_bookmark(self, path):
            self._context.bookmarks.add(path)

        @async
        def change_dir(self, path):
            try:
                self._context.file_browser.change_dir(path)
            except Exception as e:
                self.error(str(e))

        def set(self, key, value):
            if key == 'volume':
                self._context.playback_controller.set_volume(value)
            else:
                raise RuntimeError('No such key: {}'.format(key))

        def get(self, key):
            if key == 'volume':
                return self._context.playback_controller.get_volume()
            else:
                raise RuntimeError('No such key: {}'.format(key))

        def error(self, string):
            self._context.command_panel.error(string)

        def help(self, command):
            # TODO
            pass


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
        self.logger = logging.getLogger('CommandHandler')

    def _format_arguments(self, args):
        if len(args) == 0: return ''
        return ','.join('\'{}\''.format(arg.strip().replace('\'', '\\\'')) for arg in args)

    def _command_mode(self, command):
        splitted = shlex.split(command)
        command = splitted[0]
        args = splitted[1:]
        if command in self.command_mapping:
            command = self.command_mapping[command]
        if not hasattr(self.commands, command):
            raise RuntimeError('no such command: ' + command)
        eval('self.commands.{}({})'.format(command, self._format_arguments(args)))

    def _search_forward_mode(self, command):
        self.context.view.focus.searchable_list().search_forward(command)

    def _search_backward_mode(self, command):
        self.context.view.focus.searchable_list().search_backward(command)

    def list_commands(self):
        import inspect
        commands = [x[0] for x in inspect.getmembers(self.commands, predicate=inspect.ismethod) if not x[0].startswith('_')]
        commands.extend(self.command_mapping.keys())
        return commands

    def __call__(self, command):
        if not command: return
        if command.startswith(':'):
            mode = self.Mode.COMMAND
        elif command.startswith('/'):
            mode = self.Mode.SEARCH_FORWARD
        elif command.startswith('?'):
            mode = self.Mode.SEARCH_BACKWARD
        else:
            raise RuntimeError('Bad mode!')
        try:
            self.mode_map[mode](command[1:])
        except (RuntimeError, AttributeError, IndexError, TypeError, KeyError, SyntaxError, AssertionError) as exc:
            self.commands.error(str(exc))

