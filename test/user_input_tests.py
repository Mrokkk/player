#!/usr/bin/env python3

from unittest import TestCase
from unittest.mock import Mock, MagicMock, patch
from playerlib.user_input import *

class TestUserInput(TestCase):

    def setUp(self):
        self.view_mock = Mock()
        self.command_handler_mock = Mock()
        self.command_panel_mock = Mock()
        self.error_handler_mock = Mock()
        self.command_panel_mock.activation_keys = [':', '/', '?']
        self.sut = UserInput(self.view_mock, self.command_handler_mock,
                self.command_panel_mock, self.error_handler_mock)
        self.sut.key_to_command_mapping = {}

    def test_can_handle_not_mapped_key(self):
        self.view_mock.unhandled_input.return_value = True
        self.sut.handle_input('a')
        self.view_mock.unhandled_input.assert_called_once_with('a')

    def test_can_handle_not_mapped_key_and_change_focus(self):
        self.view_mock.unhandled_input.return_value = False
        self.sut.handle_input('a')
        self.view_mock.unhandled_input.assert_called_once_with('a')

    def test_can_handle_activation_keys(self):
        self.sut.handle_input(':')
        self.view_mock.focus_command_panel.assert_called_once()
        self.command_panel_mock.activate.assert_called_once_with(':')

    def test_can_handle_mapped_key(self):
        self.sut.key_to_command_mapping = {'a': ':some_command'}
        self.sut.handle_input('a')
        self.command_handler_mock.execute.assert_called_once_with(':some_command')

    def test_calls_error_handler_if_command_raises_exception(self):
        self.sut.key_to_command_mapping = {'a': ':some_command'}
        self.command_handler_mock.execute.side_effect = RuntimeError('Some error')
        self.sut.handle_input('a')
        self.command_handler_mock.execute.assert_called_once_with(':some_command')
        self.error_handler_mock.assert_called_once_with('Some error')
