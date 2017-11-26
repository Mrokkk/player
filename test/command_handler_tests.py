#!/usr/bin/env python3

import os
import sys
from unittest import TestCase
from unittest.mock import Mock, MagicMock, patch

from playerlib.player_context import *

class CommandHandlerTests(TestCase):

    def setUp(self):
        patch('playerlib.async.async', lambda x: x).start()
        import playerlib.command_handler
        self.context = PlayerContext()
        self.context.playlist = Mock()
        self.context.playback_controller = Mock()
        self.context.command_panel = Mock()
        self.context.view = Mock()
        self.context.quit = Mock()
        self.sut = playerlib.command_handler.CommandHandler(self.context)


    def test_can_execute_player_controller_commands(self):
        self.sut(':quit')
        self.context.quit.assert_called_once()


    def test_can_execute_playlist_commands(self):
        self.sut(':add_to_playlist some_file')
        self.context.playlist.add_to_playlist.assert_called_once_with('some_file')

        self.sut(':save_playlist some_file')
        self.context.playlist.save_playlist.assert_called_once_with('some_file')

        self.sut(':load_playlist some_file')
        self.context.playlist.load_playlist.assert_called_once_with('some_file')


    def test_can_execute_playback_controller_commands(self):
        self.sut(':pause')
        self.context.playback_controller.pause.assert_called_once()

        self.sut(':stop')
        self.context.playback_controller.stop.assert_called_once()

        self.sut(':next')
        self.context.playback_controller.next.assert_called_once()

        self.sut(':prev')
        self.context.playback_controller.prev.assert_called_once()

        self.sut(':seek 50%')
        self.context.playback_controller.seek.assert_called_once_with('50%')

        self.sut(':set volume 20')
        self.context.playback_controller.set_volume.assert_called_once_with('20')

        self.sut(':get volume')
        self.context.playback_controller.get_volume.assert_called_once()


    def test_can_execute_view_commands(self):
        self.sut(':switch_panes')
        self.context.view.switch_panes.assert_called_once()


    def test_bad_command_shows_error(self):
        bad_commands = [':plya', ':run', ':start', ':spot', '::']
        for cmd in bad_commands:
            self.sut(cmd)
            self.context.command_panel.error.assert_called_once()
            self.context.command_panel.error.reset_mock()


    def test_can_seek_forward(self):
        # FIXME
        self.sut('/some_string')
        self.context.view.focus.searchable_list.assert_called_once()


    def test_can_seek_backward(self):
        # FIXME
        self.sut('?some_string')
        self.context.view.focus.searchable_list.assert_called_once()


    def test_can_call_mapped_commands(self):
        self.sut(':q')
        self.context.quit.assert_called_once()


    def test_ignores_empty_command(self):
        # FIXME
        self.sut('')


    def test_cannot_set_bad_key(self):
        self.sut(':set aaakkkk value')
        self.context.command_panel.error.assert_called_once()
        self.context.command_panel.error.reset_mock()
        self.sut(':set key value')
        self.context.command_panel.error.assert_called_once()
        self.context.command_panel.error.reset_mock()
        self.sut(':set vcbx value')
        self.context.command_panel.error.assert_called_once()
        self.context.command_panel.error.reset_mock()


    def test_cannot_get_bad_key(self):
        self.sut(':get aaakkk')
        self.context.command_panel.error.assert_called_once()
        self.context.command_panel.error.reset_mock()
        self.sut(':get key')
        self.context.command_panel.error.assert_called_once()
        self.context.command_panel.error.reset_mock()
        self.sut(':get vcbx')
        self.context.command_panel.error.assert_called_once()
        self.context.command_panel.error.reset_mock()


    def test_can_properly_list_commands(self):
        commands = self.sut.list_commands()
        bad_commands = [x for x in commands if x.startswith('_')]
        self.assertEqual(len(bad_commands), 0)
        self.assertGreater(len(commands), 0)

