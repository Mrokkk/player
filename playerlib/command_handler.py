#!/usr/bin/env python3

import enum
import logging
import shlex
import urwid
from playerlib.helpers.asynchronous import *

class CommandHandler:

    class Mode(enum.Enum):
        COMMAND = ':'
        SEARCH_FORWARD = '/'
        SEARCH_BACKWARD = '?'

    class Commands:
        def __init__(self, context):
            self._context = context

        def quit(self):
            self._context.quit()

        @asynchronous
        def add_to_playlist(self, path):
            self._context.playlist.add_to_playlist(path)

        @asynchronous
        def replace_playlist(self, path):
            self._context.playlist.add_to_playlist(path, clear=True)

        def clear_playlist(self):
            self._context.playlist.clear()

        @asynchronous
        def save_playlist(self, playlist_file):
            self._context.playlist.save_playlist(playlist_file)

        @asynchronous
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

        def toggle_pane_view(self):
            self._context.view.toggle_pane_view()

        def add_bookmark(self, path):
            self._context.bookmarks.add(path)

        @asynchronous
        def change_dir(self, path):
            self._context.file_browser.change_dir(path)

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
        try: mode = [e for e in self.Mode if e.value == command[0]][0]
        except IndexError:
            self.commands.error('bad mode')
            return
        try: self.mode_map[mode](command[1:])
        except urwid.ExitMainLoop:
            raise
        except Exception as exc:
            self.commands.error(str(exc))

