#!/usr/bin/env python3

import os
import sys
from unittest import TestCase
from unittest.mock import Mock, MagicMock, patch

from playerlib.command_panel import *

class TestClamp(TestCase):
    def test_can_clamp_values(self):
        self.assertEqual(20, clamp(0, min_val=20))
        self.assertEqual(20, clamp(340, max_val=20))
        self.assertEqual(20, clamp(340, min_val=20, max_val=20))


class TestCommandPanel(TestCase):

    def setUp(self):
        self.command_handler_mock = Mock()
        self.command_handler_mock.list_commands.return_value = []
        self.sut = CommandPanel(self.command_handler_mock)
        self.sut.set_edit_text = Mock()
        self.sut.set_caption = Mock()
        self.sut.set_edit_pos = Mock()
        self.sut.get_edit_text = Mock()

    def activate_and_call(self, command):
        self.sut.activate(':')
        self.sut.get_edit_text.return_value = command
        self.sut.unhandled_input('enter')

    def reset_mocks(self):
        self.sut.set_edit_text.reset_mock()
        self.sut.set_caption.reset_mock()

    def test_can_clear_view(self):
        self.sut.clear()
        self.sut.set_edit_text.assert_called_with('')
        self.sut.set_caption.assert_called_with('')

    def test_can_display_error(self):
        self.sut.error('Some error')
        self.sut.set_edit_text.assert_called_with('')
        self.sut.set_caption.assert_called_with(('error', 'Error: Some error'))

    def test_can_display_info(self):
        self.sut.info('Some info')
        self.sut.set_edit_text.assert_called_with('')
        self.sut.set_caption.assert_called_with(('info', 'Info: Some info'))

    def test_can_be_activated(self):
        self.sut.activate(':')
        self.sut.set_edit_text.assert_called_with('')
        self.sut.set_caption.assert_called_with(':')

    def test_can_call_command(self):
        self.sut.activate(':')
        self.sut.get_edit_text.return_value = 'command'
        self.sut.unhandled_input('enter')
        self.command_handler_mock.execute.assert_called_once_with('command')

    def test_can_catch_exception_from_command(self):
        self.sut.activate(':')
        self.sut.get_edit_text.side_effect = RuntimeError('some error')
        self.sut.unhandled_input('enter')
        self.sut.set_caption.assert_called_with(('error', 'Error: some error'))

    def test_can_exit(self):
        self.sut.activate(':')
        self.sut.unhandled_input('esc')
        self.sut.set_edit_text.assert_called_with('')
        self.sut.set_caption.assert_called_with('')

    def test_displays_nothing_when_no_items_in_history(self):
        self.sut.activate(':')
        self.reset_mocks()
        self.sut.unhandled_input('up')
        self.sut.set_edit_text.assert_not_called()

        self.sut.activate(':')
        self.reset_mocks()
        self.sut.unhandled_input('down')
        self.sut.set_edit_text.assert_not_called()

    def test_can_display_previous_history_entry(self):
        self.activate_and_call('command1')
        self.sut.activate(':')
        self.reset_mocks()
        self.sut.unhandled_input('up')
        self.sut.set_edit_text.assert_called_once_with('command1')

    def test_displays_none_when_trying_to_see_current_command(self):
        self.activate_and_call('command1')
        self.sut.activate(':')
        self.reset_mocks()
        self.sut.unhandled_input('up')
        self.sut.set_edit_text.reset_mock()
        self.sut.set_caption.reset_mock()
        self.sut.unhandled_input('down')
        self.sut.set_edit_text.assert_called_once_with('')

    def test_can_display_next_item_in_history(self):
        self.activate_and_call('command1')
        self.activate_and_call('command2')
        self.sut.activate(':')
        self.sut.unhandled_input('up')
        self.sut.unhandled_input('up')
        self.reset_mocks()
        self.sut.unhandled_input('down')
        self.sut.set_edit_text.assert_called_once_with('command2')

    def test_tab_keypress_calls_completer_for_command_mode(self):
        self.sut.completer = Mock()
        self.sut.activate(':')
        self.sut.unhandled_input('tab')
        self.sut.completer.complete.assert_called_once()

    def test_tab_keypress_does_not_call_completer_on_other_modes(self):
        self.sut.completer = Mock()
        self.sut.activate('/')
        self.sut.unhandled_input('tab')
        self.sut.completer.complete.assert_not_called()
        self.sut.activate('?')
        self.sut.unhandled_input('tab')
        self.sut.completer.complete.assert_not_called()

    def test_handle_input_ignores_other_keys(self):
        self.sut.activate(':')
        self.assertEqual(self.sut.unhandled_input('a'), True)
        self.assertEqual(self.sut.unhandled_input('b'), True)

