#!/usr/bin/env python3

import os
import urwid

class Cli:

    def handle_command(self, command):
        if not command: return True
        if command == 'q' or command == 'qa':
            raise urwid.ExitMainLoop()
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


