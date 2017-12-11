#!/usr/bin/env python3

import urwim.app

class DefaultCommands:

    def error(self, string):
        urwim.App().command_panel.error(string)

    def switch_panes(self):
        urwim.App().window.switch_panes()

    def toggle_pane_view(self):
        urwim.App().window.toggle_pane_view()

    def quit(self):
        urwim.App().quit()

