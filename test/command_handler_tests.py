#!/usr/bin/env python3

import urwid
from unittest import TestCase
from unittest.mock import Mock, patch

from playerlib.context import *

class CommandHandlerTests(TestCase):

    def setUp(self):
        self.command_handler_mock = Mock()
        self.command_panel_mock = Mock()
        self.window_mock = Mock()
        self.app_instance = Mock()
        self.app_instance.command_handler = self.command_handler_mock
        self.app_instance.command_panel = self.command_panel_mock
        self.app_instance.window = self.window_mock
        self.app_mock = Mock()
        self.app_mock.return_value = self.app_instance

        patch('playerlib.helpers.asynchronous.asynchronous', lambda x: x).start()
        patch('playerlib.helpers.app.App', self.app_mock).start()
        patch('playerlib.helpers.default_commands.App', self.app_mock).start()
        import playerlib.commands
        import playerlib.helpers.command_handler
        self.context = Context()
        self.context.file_browser = Mock()
        self.context.bookmarks = Mock()
        self.context.playlist = Mock()
        self.context.playback_controller = Mock()
        self.context.command_panel = Mock()
        self.context.window = Mock()
        self.context.quit = Mock()
        self.commands = playerlib.commands.Commands(self.context)
        self.sut = playerlib.helpers.command_handler.CommandHandler(self.commands)


    def test_can_execute_player_controller_commands(self):
        self.sut(':quit')
        self.app_instance.quit.assert_called_once()


    def test_can_execute_playlist_commands(self):
        self.sut(':add_to_playlist some_file')
        self.context.playlist.add_to_playlist.assert_called_once_with('some_file')

        self.sut(':save_playlist some_file')
        self.context.playlist.save_playlist.assert_called_once_with('some_file')

        self.sut(':load_playlist some_file')
        self.context.playlist.load_playlist.assert_called_once_with('some_file')

        self.sut(':clear_playlist')
        self.context.playlist.clear.assert_called_once()

        self.context.playlist.add_to_playlist.reset_mock()
        self.sut(':replace_playlist some_file')
        self.context.playlist.add_to_playlist.assert_called_once_with('some_file', clear=True)


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


    def test_can_execute_bookmarks_commands(self):
        self.sut(':add_bookmark /path')
        self.context.bookmarks.add.assert_called_once_with('/path')


    def test_can_execute_view_commands(self):
        self.sut(':switch_panes')
        self.window_mock.switch_panes.assert_called_once()

        self.sut(':toggle_pane_view')
        self.window_mock.toggle_pane_view.assert_called_once()


    def test_can_execute_file_browser_commands(self):
        self.sut(':change_dir /path')
        self.context.file_browser.change_dir.assert_called_once_with('/path')


    def test_bad_command_shows_error(self):
        bad_commands = [':plya', ':run', ':start', ':spot', '::', 'aa']
        for cmd in bad_commands:
            self.sut(cmd)
            self.command_panel_mock.error.assert_called_once()
            self.command_panel_mock.error.reset_mock()


    # TODO
    # def test_can_seek_forward(self):
        # list_mock = Mock()
        # self.context.window.focus.searchable_list.return_value = list_mock
        # self.sut('/some_string')
        # self.context.window.focus.searchable_list.assert_called_once()
        # list_mock.search_forward.assert_called_once_with('some_string')


    # def test_can_seek_backward(self):
        # list_mock = Mock()
        # self.context.window.focus.searchable_list.return_value = list_mock
        # self.sut('?some_string')
        # self.context.window.focus.searchable_list.assert_called_once()
        # list_mock.search_backward.assert_called_once_with('some_string')


    def test_can_call_mapped_commands(self):
        self.sut(':q')
        self.app_instance.quit.assert_called_once()


    def test_ignores_empty_command(self):
        self.sut('')
        self.command_panel_mock.error.assert_not_called()


    def test_cannot_set_bad_key(self):
        self.sut(':set aaakkkk value')
        self.command_panel_mock.error.assert_called_once()
        self.command_panel_mock.error.reset_mock()
        self.sut(':set key value')
        self.command_panel_mock.error.assert_called_once()
        self.command_panel_mock.error.reset_mock()
        self.sut(':set vcbx value')
        self.command_panel_mock.error.assert_called_once()
        self.command_panel_mock.error.reset_mock()


    def test_cannot_get_bad_key(self):
        self.sut(':get aaakkk')
        self.command_panel_mock.error.assert_called_once()
        self.command_panel_mock.error.reset_mock()
        self.sut(':get key')
        self.command_panel_mock.error.assert_called_once()
        self.command_panel_mock.error.reset_mock()
        self.sut(':get vcbx')
        self.command_panel_mock.error.assert_called_once()
        self.command_panel_mock.error.reset_mock()


    def test_can_properly_list_commands(self):
        commands = self.sut.list_commands()
        bad_commands = [x for x in commands if x.startswith('_')]
        self.assertEqual(len(bad_commands), 0)
        self.assertGreater(len(commands), 0)

