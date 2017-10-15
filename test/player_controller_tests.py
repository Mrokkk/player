#!/usr/bin/env python3

from unittest import TestCase
from unittest.mock import Mock, MagicMock, patch, call
from playerlib.player_controller import *

from urwid import ExitMainLoop

class PLayerControllerTests(TestCase):

    def setUp(self):
        self.context_mock = Mock()
        self.context_mock.draw_lock = MagicMock()

        self.current_track_mock = Mock()
        self.current_track_mock.title = ''
        self.current_track_mock.offset = 0
        self.current_track_mock.length = 0

        self.playback_controller_mock = Mock()
        self.playback_controller_mock.current_track = self.current_track_mock

        self.command_panel_mock = Mock()
        self.view_mock = Mock()
        self.playlist_mock = Mock()

        self.context_mock.playback_controller = self.playback_controller_mock
        self.context_mock.command_panel = self.command_panel_mock
        self.context_mock.view = self.view_mock
        self.context_mock.playlist = self.playlist_mock

        self.sut = PlayerController(self.context_mock)
        self.sut.tracks_factory = Mock()


    def test_can_quit_program(self):
        self.assertRaises(ExitMainLoop, self.sut.quit)


    def test_ignores_negative_value(self):
        self.sut.update_current_state(-1)
        self.sut.update_current_state(-10)
        self.sut.update_current_state(-21)
        self.command_panel_mock.set_caption.assert_not_called()


    def test_can_update_current_track_time_position(self):
        self.current_track_mock.offset = 0
        self.current_track_mock.length = 20
        self.current_track_mock.title = 'Some Title'

        self.sut.update_current_state(1)
        self.command_panel_mock.set_caption.assert_called_once_with('Some Title : 00:01 / 00:20')
        self.command_panel_mock.set_caption.reset_mock()

        self.sut.update_current_state(10)
        self.command_panel_mock.set_caption.assert_called_once_with('Some Title : 00:10 / 00:20')
        self.command_panel_mock.set_caption.reset_mock()

        self.sut.update_current_state(11)
        self.command_panel_mock.set_caption.assert_called_once_with('Some Title : 00:11 / 00:20')
        self.command_panel_mock.set_caption.reset_mock()

        self.sut.update_current_state(11)
        self.command_panel_mock.set_caption.assert_called_once_with('Some Title : 00:11 / 00:20')
        self.command_panel_mock.set_caption.reset_mock()


    def test_can_update_current_track_time_position_when_track_length_longer_than_hour(self):
        self.current_track_mock.offset = 0
        self.current_track_mock.length = 7200
        self.current_track_mock.title = 'Some Title'

        self.sut.update_current_state(1)
        self.command_panel_mock.set_caption.assert_called_once_with('Some Title : 00:00:01 / 02:00:00')
        self.command_panel_mock.set_caption.reset_mock()

        self.sut.update_current_state(100)
        self.command_panel_mock.set_caption.assert_called_once_with('Some Title : 00:01:40 / 02:00:00')
        self.command_panel_mock.set_caption.reset_mock()


    def test_can_go_to_next_track(self):
        self.current_track_mock.offset = 0
        self.current_track_mock.length = 32
        self.current_track_mock.title = 'Some Title'
        next_track_mock = Mock()
        next_track_mock.offset = 32
        next_track_mock.length = 21
        next_track_mock.title = 'Some Other Title'
        self.current_track_mock.playlist_entry.next.track = next_track_mock

        self.sut.update_current_state(10)
        self.command_panel_mock.set_caption.assert_called_once_with('Some Title : 00:10 / 00:32')
        self.command_panel_mock.set_caption.reset_mock()

        self.sut.update_current_state(32)
        self.command_panel_mock.set_caption.assert_called_once_with('Some Other Title : 00:00 / 00:21')
        self.command_panel_mock.set_caption.reset_mock()

        self.sut.update_current_state(42)
        self.command_panel_mock.set_caption.assert_called_once_with('Some Other Title : 00:10 / 00:21')
        self.command_panel_mock.set_caption.reset_mock()


    def test_ignores_if_footer_focused(self):
        self.current_track_mock.offset = 0
        self.current_track_mock.length = 104
        self.current_track_mock.title = 'Some Title'
        self.view_mock.focus_position = 'footer'

        self.sut.update_current_state(42)
        self.sut.update_current_state(32)
        self.sut.update_current_state(3)
        self.command_panel_mock.set_caption.assert_not_called()


    def test_can_add_tracks_to_playlist(self):
        track1 = Mock()
        track2 = Mock()
        self.sut.tracks_factory.get.return_value = [track1, track2]
        self.sut.add_to_playlist('/some/path')
        self.playlist_mock.add.assert_has_calls([call(track1), call(track2)])


    def test_can_clear_playlist_and_add_tracks(self):
        track1 = Mock()
        track2 = Mock()
        self.sut.tracks_factory.get.return_value = [track1, track2]
        self.sut.add_to_playlist('/some/path', clear=True)
        self.playlist_mock.clear.assert_called_once()
        self.playlist_mock.add.assert_has_calls([call(track1), call(track2)])


    def test_raises_exception_when_no_tracks_returned_from_tracks_factory(self):
        self.sut.tracks_factory.get.return_value = []
        self.assertRaises(RuntimeError, self.sut.add_to_playlist, '/some/path')
        self.sut.tracks_factory.get.return_value = None
        self.assertRaises(RuntimeError, self.sut.add_to_playlist, '/some/path')

