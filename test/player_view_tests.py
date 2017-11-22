#!/usr/bin/env python3

from unittest import TestCase
from unittest.mock import Mock

from playerlib.player_view import *

class PlayerViewTests(TestCase):

    def setUp(self):
        self.file_browser_mock = Mock()
        self.playlist_mock = Mock()
        self.command_panel_mock = Mock()
        self.columns_mock = Mock()
        self.sut = PlayerView(self.file_browser_mock, self.playlist_mock, self.command_panel_mock)

    def test_on_start_file_browser_is_focused(self):
        self.assertEqual(self.sut.focus, self.file_browser_mock)

    def test_can_switch_focus_between_widgets(self):
        self.sut.switch_panes()
        self.assertEqual(self.sut.focus, self.playlist_mock)
        self.sut.switch_panes()
        self.assertEqual(self.sut.focus, self.file_browser_mock)
        self.sut.switch_panes()
        self.assertEqual(self.sut.focus, self.playlist_mock)

    def test_should_pass_keys_to_the_widgets(self):
        self.sut.unhandled_input('a')
        self.file_browser_mock.unhandled_input.assert_called_once_with('a')
        self.playlist_mock.unhandled_input.assert_not_called()
        self.file_browser_mock.unhandled_input.reset_mock()
        self.sut.switch_panes()
        self.sut.unhandled_input('b')
        self.file_browser_mock.unhandled_input.assert_not_called()
        self.playlist_mock.unhandled_input.assert_called_once_with('b')
        self.playlist_mock.unhandled_input.reset_mock()
        self.sut.switch_panes()
        self.sut.unhandled_input('c')
        self.file_browser_mock.unhandled_input.assert_called_once_with('c')
        self.playlist_mock.unhandled_input.assert_not_called()
        self.file_browser_mock.unhandled_input.reset_mock()

    def test_should_pass_key_to_command_panel_if_footer_is_focused(self):
        self.sut.focus_command_panel()
        self.sut.unhandled_input('d')
        self.file_browser_mock.unhandled_input.assert_not_called()
        self.playlist_mock.unhandled_input.assert_not_called()
        self.file_browser_mock.unhandled_input.reset_mock()
        self.command_panel_mock.unhandled_input.assert_called_once_with('d')
        self.command_panel_mock.unhandled_input.reset_mock()

        self.sut.focus_body()
        self.sut.unhandled_input('e')
        self.command_panel_mock.unhandled_input.assert_not_called()

