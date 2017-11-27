#!/usr/bin/env python3

import os
import sys
from unittest import TestCase
from unittest.mock import Mock, MagicMock
from playerlib.playback_controller import *

class PlaybackControllerTests(TestCase):

    def setUp(self):
        self.command_panel_mock = Mock()
        self.view_mock = Mock()

        self.context_mock = Mock()
        self.context_mock.command_panel = self.command_panel_mock
        self.context_mock.view = self.view_mock
        self.context_mock.draw_lock = MagicMock()
        self.context_mock.config.backend = 'mplayer'
        self.command_panel_mock.selectable.return_value = False

        self.current_track_mock = Mock()

        self.sut = PlaybackController(self.context_mock)

        self.backend = Mock()
        self.sut.backend = self.backend

    def test_play_will_raise_exception_when_no_track_given(self):
        self.assertRaises(RuntimeError, self.sut.play_track, None)

    def test_play_sets_current_track(self):
        self.sut.play_track(Mock())
        self.assertNotEqual(self.sut.current_track, None)

    def test_play_sends_track_to_backend(self):
        track = Mock()
        self.sut.play_track(track)
        self.backend.play_track.assert_called_with(track)

    def test_play_will_stop_current_track_if_exists(self):
        track = Mock()
        last_track = MagicMock()
        self.sut.current_track = last_track
        self.sut.play_track(track)

    def test_quit_will_stop_backend_if_it_exists(self):
        self.sut.backend = self.backend
        self.sut.quit()
        self.backend.quit.assert_called_once()

    def test_stop_will_raise_exception_when_no_track_playing(self):
        self.assertRaises(RuntimeError, self.sut.stop)

    def test_stop_will_send_stop_to_backend_if_track_is_playing(self):
        track = Mock()
        self.sut.current_track = track
        self.sut.backend = self.backend
        self.sut.stop()
        self.backend.stop.assert_called_once()

    def test_pause_will_raise_exception_when_no_track_playing(self):
        self.assertRaises(RuntimeError, self.sut.pause)

    def test_pause_calls_toggle_pause(self):
        track = Mock()
        self.sut.current_track = track
        self.sut.backend = self.backend
        self.sut.pause()
        self.backend.toggle_pause.assert_called_once()

    def test_can_seek_with_proper_values(self):
        track = Mock()
        self.sut.current_track = track
        self.sut.backend = self.backend
        self.sut.seek('60%')
        self.backend.seek_percentage.assert_called_once_with(60)
        self.sut.seek('+10')
        self.backend.seek_forward.assert_called_once_with(10)
        self.sut.seek('-10')
        self.backend.seek_backward.assert_called_once_with(10)
        self.sut.seek('90')
        self.backend.seek.assert_called_once_with(90)

    def test_will_raise_exception_on_improper_seek_values(self):
        values = ['10%%', '%1%', '-10+', '', ' ', '+-', '#', '[', ']', '+9*', '-094+_']
        track = Mock()
        self.sut.current_track = track
        self.sut.backend = self.backend
        for value in values:
            self.assertRaises(Exception, self.sut.seek, value)

    def test_seek_will_raise_exception_when_no_track_playing(self):
        self.assertRaises(Exception, self.sut.seek, '3')
        self.assertRaises(Exception, self.sut.seek, '+3')
        self.assertRaises(Exception, self.sut.seek, '-3')
        self.assertRaises(Exception, self.sut.seek, '3%')

    def test_next_and_prev_will_raise_exception_in_no_track_playing(self):
        self.sut.current_track = None
        self.assertRaises(Exception, self.sut.next)
        self.assertRaises(Exception, self.sut.prev)

    def test_next_will_stop_if_no_track_and_current_track_playing(self):
        track = Mock()
        track.playlist_entry.next = None
        self.sut.current_track = track
        self.sut.backend = self.backend
        self.sut.next()
        self.backend.play_track.assert_not_called()
        self.backend.stop.assert_called_once()

    def test_next_will_play_next_track(self):
        track = Mock()
        next_track = Mock()
        track.playlist_entry.next.track = next_track
        self.sut.current_track = track
        self.sut.backend = self.backend
        self.sut.next()
        self.backend.play_track.assert_called_with(next_track)

    def test_prev_will_stop_if_no_track_and_current_track_playing(self):
        track = Mock()
        track.playlist_entry = Mock()
        track.playlist_entry.prev = None
        self.sut.current_track = track
        self.sut.backend = self.backend
        self.sut.prev()
        self.backend.play_track.assert_not_called()
        self.backend.stop.assert_called_once()

    def test_prev_will_play_prev_track(self):
        track = Mock()
        prev_track = Mock()
        track.playlist_entry.prev.track = prev_track
        self.sut.current_track = track
        self.sut.backend = self.backend
        self.sut.prev()
        self.backend.play_track.assert_called_with(prev_track)

    def test_ignores_negative_value(self):
        self.sut.current_track = self.current_track_mock
        self.sut.update_current_state(-1)
        self.sut.update_current_state(-10)
        self.sut.update_current_state(-21)
        self.command_panel_mock.set_caption.assert_not_called()


    def test_can_update_current_track_time_position(self):
        self.current_track_mock.offset = 0
        self.current_track_mock.length = 20
        self.current_track_mock.length_string = '00:20'
        self.current_track_mock.time_format = '%M:%S'
        self.current_track_mock.title = 'Some Title'
        self.sut.current_track = self.current_track_mock

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


    def test_can_go_to_next_track(self):
        self.current_track_mock.offset = 0
        self.current_track_mock.length = 32
        self.current_track_mock.title = 'Some Title'
        self.current_track_mock.path = '/path'
        self.current_track_mock.length_string = '00:32'
        self.current_track_mock.time_format = '%M:%S'
        next_track_mock = Mock()
        next_track_mock.offset = 32
        next_track_mock.length = 21
        next_track_mock.title = 'Some Other Title'
        next_track_mock.path = '/path'
        next_track_mock.length_string = '00:21'
        next_track_mock.time_format = '%M:%S'
        self.current_track_mock.playlist_entry.next.track = next_track_mock
        self.sut.current_track = self.current_track_mock

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
        self.command_panel_mock.selectable.return_value = True
        self.current_track_mock.offset = 0
        self.current_track_mock.length = 104
        self.current_track_mock.title = 'Some Title'
        self.sut.current_track = self.current_track_mock
        self.view_mock.focus_position = 'footer'

        self.sut.update_current_state(42)
        self.sut.update_current_state(32)
        self.sut.update_current_state(3)
        self.command_panel_mock.set_caption.assert_not_called()


    def test_can_set_volume(self):
        self.sut.set_volume('42')
        self.backend.set_volume.assert_called_once_with(42)
        self.backend.set_volume.reset_mock()
        self.sut.set_volume('+42')
        self.backend.set_volume.assert_called_once_with(84)
        self.backend.set_volume.reset_mock()
        self.sut.set_volume('-20')
        self.backend.set_volume.assert_called_once_with(64)
        self.backend.set_volume.reset_mock()
        self.sut.set_volume('100')
        self.backend.set_volume.assert_called_once_with(100)


    def test_volume_level_clamps_to_range_0_100(self):
        self.sut.set_volume('-102')
        self.backend.set_volume.assert_called_once_with(0)
        self.backend.set_volume.reset_mock()
        self.sut.set_volume('1534')
        self.backend.set_volume.assert_called_once_with(100)


    def test_setting_same_volume_is_ignored(self):
        self.sut.set_volume('20')
        self.backend.set_volume.assert_called_once_with(20)
        self.backend.set_volume.reset_mock()
        self.sut.set_volume('20')
        self.backend.set_volume.assert_not_called()


    def test_can_read_volume(self):
        self.sut.set_volume('42')
        self.assertEqual(self.sut.get_volume(), 42)

