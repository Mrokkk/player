#!/usr/bin/env python3

import urwim.app
import urwim.rdb

class DefaultCommands:

    def error(self, string):
        urwim.App().command_panel.error(string)

    def info(self, string):
        urwim.App().command_panel.info(string)

    def switch_panes(self):
        urwim.App().window.switch_panes()

    def toggle_pane_view(self):
        urwim.App().window.toggle_pane_view()

    def quit(self):
        urwim.App().quit()

    def get(self, key):
        value = urwim.Rdb()[key]
        self.info('{}: {}'.format(key, value))
        return value

    def set(self, key, value):
        old_value = urwim.Rdb()[key]
        if '+' in value:
            new_value = old_value + int(value[1:])
        elif '-' in value:
            new_value = old_value - int(value[1:])
        else:
            new_value = int(value)
        urwim.Rdb()[key] = new_value

