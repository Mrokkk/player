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
            return True
        elif command == 'pause':
            self.player.toggle_pause()
            return True
        elif command == 'stop':
            self.player.stop()
            return True
        elif command == 'next':
            self.player.next()
            return True
        elif command == 'prev':
            self.player.prev()
            return True
        elif command == 'e':
            self.player.add_to_playlist(args[0])
            return True
        else:
            raise RuntimeError('No such command: ' + command)

    def _search_forward_mode(self, command):
        self.player.panes.search_forward(command)
        return True

    def _search_backward_mode(self, command):
        # TODO
        return True

    def handle_command(self, command, mode):
        if not command: return True
        return self.mode_map[mode](command)


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

    def unhandled_input(self, key):
        if key == 'enter':
            try:
                if self.cli.handle_command(self.get_edit_text().strip(), self.mode):
                    self._clear_and_set_caption('')
            except (RuntimeError, AttributeError) as exc:
                self._clear_and_set_caption(('error', exc.__str__()))
        elif key == 'esc':
            self._clear_and_set_caption('')
        elif key == 'up':
            # TODO
            return True
        elif key == 'down':
            # TODO
            return True

