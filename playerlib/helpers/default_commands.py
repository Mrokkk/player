#!/usr/bin/env python3

from playerlib.helpers.app import *

class DefaultCommands:

    def error(self, string):
        App().command_panel.error(string)

    def switch_panes(self):
        App().window.switch_panes()

    def toggle_pane_view(self):
        App().window.toggle_pane_view()

    def quit(self):
        App().quit()

