#!/usr/bin/env python3

import os
import urwid

class CliMode:
    COMMAND = 1
    SEARCH_FORWARD = 2
    SEARCH_BACKWARD = 3


class Cli:

    def __init__(self, player):
        self.player = player
        self.mode_map = {
            CliMode.COMMAND: self._command_mode,
            CliMode.SEARCH_FORWARD: self._search_forward_mode,
            CliMode.SEARCH_BACKWARD: self._search_backward_mode
        }

    def _command_mode(self, command):
        splitted = command.split()
        command = splitted[0]
        args = splitted[1:]
        if command == 'q' or command == 'qa':
            self.player.quit()
        elif command == 'pause':
            self.player.toggle_pause()
        elif command == 'stop':
            self.player.stop()
        elif command == 'next':
            self.player.next()
        elif command == 'prev':
            self.player.prev()
        elif command == 'e':
            self.player.add_to_playlist(args[0])
        else:
            raise RuntimeError('No such command: ' + command)

    def _search_forward_mode(self, command):
        self.player.panes.search_forward(command)

    def _search_backward_mode(self, command):
        # TODO
        pass

    def handle_command(self, command, mode):
        if not command: return
        self.mode_map[mode](command)


class CliPanel(urwid.Edit):

    def __init__(self, cli):
        super().__init__()
        self.cli = cli
        self.mode = CliMode.COMMAND

    def _clear_and_set_caption(self, caption):
        self.set_edit_text('')
        self.set_caption(caption)

    def set_mode(self, mode):
        self.mode = mode

    def error(self, error):
        self._clear_and_set_caption(('error', error))

    def unhandled_input(self, key):
        if key == 'enter':
            try:
                self.cli.handle_command(self.get_edit_text().strip(), self.mode)
                self._clear_and_set_caption('')
            except (RuntimeError, AttributeError, IndexError) as exc:
                self._clear_and_set_caption(('error', exc.__str__()))
        elif key == 'esc':
            self._clear_and_set_caption('')
        elif key == 'up':
            # TODO
            return True
        elif key == 'down':
            # TODO
            return True

