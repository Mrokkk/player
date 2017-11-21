#!/usr/bin/env python3

import logging
import os
import urwid
from playerlib.helpers.helpers import clamp

class Completer:

    class Context:
        def __init__(self, index, last_text, completions):
            self.index = index
            self.last_text = last_text
            self.completions = completions

    def __init__(self, commands, edit_widget):
        self.commands = sorted(commands)
        self.edit_widget = edit_widget
        self.logger = logging.getLogger('Completer')

    def _handle_no_context(self, last_word, words_count, edit_text):
        if words_count > 1:
            matched_commands = [c for c in sorted(os.listdir('.')) if c.startswith(last_word)]
        else:
            matched_commands = [c for c in self.commands if c.startswith(last_word)]
        self.logger.debug('For {} found {}'.format(last_word, matched_commands))
        if len(matched_commands) == 0: return None
        self.edit_widget.insert_text(matched_commands[0][len(last_word):])
        return self.Context(0, last_word, matched_commands)

    def _handle_context(self, context, last_word, words_count, edit_text):
        if context.last_text != last_word and not last_word in context.completions:
            self.logger.debug('Context invalidated')
            return self._handle_no_context(last_word, words_count, edit_text)
        context.index = 0 if (context.index == len(context.completions) - 1) else context.index + 1
        new_edit_text = self._replace_last_word(edit_text, context.completions[context.index])
        self.edit_widget.set_edit_text(new_edit_text)
        self.edit_widget.set_edit_pos(len(new_edit_text))
        return context

    def _replace_last_word(self, string, word):
        words = string.split()
        words[-1] = word
        return ' '.join(words)

    def _get_last_word_and_words_count(self, string):
        words = string.split()
        if len(string):
            return ('', len(words) + 1) if string[-1] == ' ' else (words[-1], len(words))
        else:
            return ('', 0)

    def complete(self, context):
        edit_text = self.edit_widget.get_edit_text()
        last_word, words_count = self._get_last_word_and_words_count(edit_text)
        return self._handle_context(context, last_word, words_count, edit_text) if context else self._handle_no_context(last_word, words_count, edit_text)


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

