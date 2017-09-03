#!/usr/bin/env python3

import os
import urwid

class Cli:

    def __init__(self, player):
        self.player = player

    def handle_command(self, command):
        if not command: return True
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


class CliPanel(urwid.Edit):

    def __init__(self, cli):
        super().__init__()
        self.cli = cli

    def _clear_and_set_caption(self, caption):
        self.set_edit_text('')
        self.set_caption(caption)

    def unhandled_input(self, key):
        if key == 'enter':
            try:
                if self.cli.handle_command(self.get_edit_text().strip()):
                    self._clear_and_set_caption('')
            except RuntimeError as exc:
                self._clear_and_set_caption(('error', exc.__str__()))

