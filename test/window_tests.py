#!/usr/bin/env python3

from unittest import TestCase
from unittest.mock import Mock, ANY

from playerlib.helpers.window import *

class PlayerViewTests(TestCase):

    def setUp(self):
        self.main_view_mock = Mock()
        self.command_panel_mock = Mock()
        self.command_panel_mock.activation_keys = [':']
        self.sut = Window(self.main_view_mock, self.command_panel_mock)

    def test_can_switch_focus_between_widgets(self):
        self.sut.switch_panes()
        self.main_view_mock.switch_panes.assert_called_once()

    def test_should_pass_keys_to_main_view_if_body_focused(self):
        self.sut.handle_input('a')
        self.main_view_mock.handle_input.assert_called_once_with('a')

    def test_should_pass_keys_to_command_panel_if_footer_focused(self):
        self.command_panel_mock.is_active.return_value = False
        self.sut.keypress(None, ':')
        self.command_panel_mock.is_active.return_value = True
        self.sut.handle_input('a')
        self.command_panel_mock.handle_input.assert_called_once_with('a', ANY)

    def test_should_focus_panel_if_command_panel_activation_key_pressed(self):
        self.command_panel_mock.is_active.return_value = False
        self.sut.keypress(None, ':')
        self.command_panel_mock.activate.assert_called_once_with(':')

