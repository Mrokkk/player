#!/usr/bin/env python3

import urwid

def clamp(value, min_val=-9999, max_val=9999):
    if value > max_val: return max_val
    if value < min_val: return min_val
    return value


class CommandPanel(urwid.Edit):

    def __init__(self, command_handler):
        super().__init__()
        self.command_handler = command_handler
        self.mode = None
        self.history_index = None
        self.activation_keys = (':', '/', '?')
        self.history = {
            self.activation_keys[0]: [],
            self.activation_keys[1]: [],
            self.activation_keys[2]: [],
        }
        self.history_index = -1

    def _clear_and_set_caption(self, caption):
        self.set_edit_text('')
        self.set_caption(caption)

    def activate(self, key):
        self.mode = key
        self._clear_and_set_caption(key)
        self.history_index = -1

    def error(self, error):
        self._clear_and_set_caption(('error', 'Error: ' + error))

    def info(self, error):
        self._clear_and_set_caption(('info', 'Info: ' + error))

    def clear(self):
        self._clear_and_set_caption('')

    def _update_panel(self):
        self.set_edit_text(self.history[self.mode][self.history_index])
        self.set_edit_pos(len(self.edit_text))

    def unhandled_input(self, key):
        if key == 'enter':
            try:
                self.history[self.mode].insert(0, self.get_edit_text().strip())
                self.command_handler.execute(self.caption + self.get_edit_text().strip())
                self.clear()
            except (RuntimeError, AttributeError, IndexError, TypeError, KeyError) as exc:
                self.error(str(exc))
        elif key == 'esc':
            self.clear()
        elif key == 'up':
            try:
                self.history_index += 1
                self.history_index = clamp(self.history_index, max_val=len(self.history[self.mode])-1)
                self._update_panel()
            except: pass
            return True
        elif key == 'down':
            if self.history_index < 0: return True
            self.history_index -= 1
            self.history_index = clamp(self.history_index, min_val=-1)
            if self.history_index == -1:
                self.set_edit_text('')
                self.set_edit_pos(0)
                return True
            self._update_panel()
            return True
        else:
            return True
