#!/usr/bin/env python3

import logging
import urwid
from playerlib.helpers.helpers import clamp

class Completer:

    class Context:
        def __init__(self, index, last_text, commands):
            self.index = index
            self.last_text = last_text
            self.commands = commands

    def __init__(self, commands, edit_widget):
        self.commands = sorted(commands)
        self.edit_widget = edit_widget
        self.logger = logging.getLogger('Completer')

    def _handle_no_context(self, edit_text):
        index = 0
        matched_commands = [c for c in self.commands if c.startswith(edit_text)]
        self.logger.debug('For {} found {}'.format(edit_text, matched_commands))
        if len(matched_commands) == 0: return None
        self.edit_widget.insert_text(matched_commands[0][len(edit_text):])
        context = self.Context(0, edit_text, matched_commands)
        return context

    def _handle_context(self, edit_text, context):
        if context.last_text != edit_text and not edit_text in context.commands:
            self.logger.debug('Context invalidated')
            return self._handle_no_context(edit_text)
        try:
            context.index += 1
            self.edit_widget.set_edit_text(context.commands[context.index])
            self.edit_widget.set_edit_pos(len(context.commands[context.index]))
        except:
            context.index = 0
            self.edit_widget.set_edit_text(context.commands[context.index])
            self.edit_widget.set_edit_pos(len(context.commands[context.index]))
        return context

    def complete(self, context):
        edit_text = self.edit_widget.get_edit_text()
        if context:
            return self._handle_context(edit_text, context)
        else:
            return self._handle_no_context(edit_text)


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
        self.completer = Completer(self.command_handler.list_commands(), self)
        self.completer_context = None
        self.logger = logging.getLogger('CommandPanel')

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

    def _handle_enter(self):
        try:
            self.history[self.mode].insert(0, self.get_edit_text().strip())
            self.command_handler.execute(self.caption + self.get_edit_text().strip())
            self.clear()
        except (RuntimeError, AttributeError, IndexError, TypeError, KeyError, SyntaxError, AssertionError) as exc:
            self.error(str(exc))

    def _handle_up_arrow(self):
        try:
            self.history_index += 1
            self.history_index = clamp(self.history_index, max_val=len(self.history[self.mode])-1)
            self._update_panel()
        except: pass
        return True

    def _handle_down_arrow(self):
        if self.history_index < 0: return True
        self.history_index -= 1
        self.history_index = clamp(self.history_index, min_val=-1)
        if self.history_index == -1:
            self.set_edit_text('')
            self.set_edit_pos(0)
            return True
        self._update_panel()
        return True

    def unhandled_input(self, key):
        if key == 'enter':
            self._handle_enter()
        elif key == 'esc':
            self.clear()
        elif key == 'up':
            return self._handle_up_arrow()
        elif key == 'down':
            return self._handle_down_arrow()
        elif key == 'tab':
            if self.mode == ':':
                self.completer_context = self.completer.complete(self.completer_context)
                return True
        else:
            return True

