#!/usr/bin/env python3

import os
import sys
from unittest import TestCase
from unittest.mock import Mock, MagicMock, patch

from playerlib.command_handler import *

class TestCommandHandler(TestCase):

    def setUp(self):
        self.context_mock = Mock()
        self.sut = CommandHandler(self.context_mock)


    def test_can_execute_player_controller_commands(self):
        self.sut.execute(':quit')
        self.context_mock.player_controller.quit.assert_called_once()

        self.sut.execute(':add_to_playlist some_file')
        self.context_mock.player_controller.add_to_playlist.assert_called_once_with('some_file')


    def test_can_execute_playback_controller_commands(self):
        self.sut.execute(':pause')
        self.context_mock.playback_controller.pause.assert_called_once()

        self.sut.execute(':stop')
        self.context_mock.playback_controller.stop.assert_called_once()

        self.sut.execute(':next')
        self.context_mock.playback_controller.next.assert_called_once()

        self.sut.execute(':prev')
        self.context_mock.playback_controller.prev.assert_called_once()

        self.sut.execute(':seek 50%')
        self.context_mock.playback_controller.seek.assert_called_once_with('50%')


    def test_can_execute_view_commands(self):
        self.sut.execute(':switch_panes')
        self.context_mock.view.switch_panes.assert_called_once()


    def test_bad_command_raises_runtime_error(self):
        bad_commands = [':plya', ':run', ':start', ':spot', '::']
        for cmd in bad_commands:
            self.assertRaises(RuntimeError, self.sut.execute, cmd)


    def test_can_seek_forward(self):
        self.sut.execute('/some_string')
        self.context_mock.view.focus.search_forward.assert_called_with('some_string')


    def test_can_seek_backward(self):
        self.sut.execute('?some_string')
        self.context_mock.view.focus.search_backward.assert_called_with('some_string')


    def test_can_call_mapped_commands(self):
        self.sut.execute(':q')
        self.context_mock.player_controller.quit.assert_called_once()


    def test_ignores_empty_command(self):
        self.sut.execute('')

