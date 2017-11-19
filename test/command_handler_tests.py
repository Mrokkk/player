#!/usr/bin/env python3

import os
import sys
from unittest import TestCase
from unittest.mock import Mock, MagicMock, patch

from playerlib.command_handler import *

class CommandHandlerTests(TestCase):

    def setUp(self):
        self.context_mock = Mock()
        self.sut = CommandHandler(self.context_mock)


    def test_can_execute_player_controller_commands(self):
        self.sut.execute(':quit')
        self.context_mock.quit.assert_called_once()


    def test_can_execute_playlist_commands(self):
        self.sut.execute(':add_to_playlist some_file')
        self.context_mock.playlist.add_to_playlist.assert_called_once_with('some_file')

        self.sut.execute(':save_playlist some_file')
        self.context_mock.playlist.save_playlist.assert_called_once_with('some_file')

        self.sut.execute(':load_playlist some_file')
        self.context_mock.playlist.load_playlist.assert_called_once_with('some_file')


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

        self.sut.execute(':set volume 20')
        self.context_mock.playback_controller.set_volume.assert_called_once_with('20')

        self.sut.execute(':get volume')
        self.context_mock.playback_controller.get_volume.assert_called_once()


    def test_can_execute_view_commands(self):
        self.sut.execute(':switch_panes')
        self.context_mock.view.switch_panes.assert_called_once()


    def test_bad_command_raises_error(self):
        bad_commands = [':plya', ':run', ':start', ':spot', '::']
        for cmd in bad_commands:
            self.assertRaises(Exception, self.sut.execute, cmd)


    def test_can_seek_forward(self):
        self.sut.execute('/some_string')
        self.context_mock.view.focus.search_forward.assert_called_with('some_string')


    def test_can_seek_backward(self):
        self.sut.execute('?some_string')
        self.context_mock.view.focus.search_backward.assert_called_with('some_string')


    def test_can_call_mapped_commands(self):
        self.sut.execute(':q')
        self.context_mock.quit.assert_called_once()


    def test_ignores_empty_command(self):
        self.sut.execute('')


    def test_cannot_set_bad_key(self):
        self.assertRaises(RuntimeError, self.sut.execute, ':set aaakkkk value')
        self.assertRaises(RuntimeError, self.sut.execute, ':set key value')
        self.assertRaises(RuntimeError, self.sut.execute, ':set vcbx value')


    def test_cannot_get_bad_key(self):
        self.assertRaises(RuntimeError, self.sut.execute, ':get aaakkk')
        self.assertRaises(RuntimeError, self.sut.execute, ':get key')
        self.assertRaises(RuntimeError, self.sut.execute, ':get vcbx')


    def test_can_properly_list_commands(self):
        commands = self.sut.list_commands()
        bad_commands = [x for x in commands if x.startswith('_')]
        self.assertEqual(len(bad_commands), 0)
        self.assertGreater(len(commands), 0)


    def test_raises_exception_on_bad_command(self):
        self.assertRaises(Exception, self.sut.execute, 'set key value')
        self.assertRaises(Exception, self.sut.execute, '\\fdsfkj')

