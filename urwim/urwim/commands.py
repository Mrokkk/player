#!/usr/bin/env python3

import urwim.app
import urwim.rdb

class Commands:

    def error(self, string: str) -> None:
        urwim.App().command_panel.error(string)

    def info(self, string: str) -> None:
        urwim.App().command_panel.info(string)

    def switch_panes(self) -> None:
        urwim.App().window.switch_panes()

    def toggle_pane_view(self) -> None:
        urwim.App().window.toggle_pane_view()

    def quit(self) -> None:
        urwim.App().quit()

    def get(self, key: str) -> None:
        value = urwim.rdb[key]
        self.info('{}: {}'.format(key, value))
        return value

    def set(self, key: str, value: str) -> None:
        old_value = urwim.rdb[key]
        if '+' in value:
            new_value = old_value + int(value[1:])
        elif '-' in value:
            new_value = old_value - int(value[1:])
        else:
            new_value = int(value)
        urwim.rdb[key] = new_value

    def tabnew(self) -> None:
        raise NotImplementedError('not implemented')

    def tabn(self) -> None:
        urwim.App().window.next_tab()

    def tabp(self) -> None:
        urwim.App().window.prev_tab()

