#!/usr/bin/env python3

import os
import sys
from unittest import TestCase
from unittest.mock import Mock, MagicMock
from playerlib.playback_controller import *

class TestPlaybackController(TestCase):

    def setUp(self):
        self.backend = Mock()
        self.backend_factory = MagicMock()
        self.backend_factory.create.return_value = self.backend
        self.sut = PlaybackController(self.backend_factory)

    def test_play_will_raise_exception_when_no_track_given(self):
        self.assertRaises(RuntimeError, self.sut.play_file, None)

    def test_play_creates_backend(self):
        self.sut.play_file(Mock())
        self.backend_factory.create.assert_called()
        self.assertNotEqual(self.sut.backend, None)

    def test_play_sets_current_track(self):
        self.sut.play_file(Mock())
        self.assertNotEqual(self.sut.current_track, None)

    def test_play_sends_track_to_backend(self):
        track = Mock()
        self.sut.play_file(track)
        self.backend.play_file.assert_called_with(track)

    def test_play_will_stop_current_track_if_exists(self):
        track = Mock()
        last_track = MagicMock()
        self.sut.current_track = last_track
        self.sut.play_file(track)

    def test_quit_will_stop_backend_if_it_exists(self):
        self.sut.backend = self.backend
        self.sut.quit()
        self.backend.quit.assert_called_once()

    def test_quit_will_do_nothing_if_backend_doesnt_exist(self):
        self.sut.quit()
        self.backend.quit.assert_not_called()

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

    def test_next_and_prev_will_raise_exception_in_no_track_playing(self):
        self.sut.current_track = None
        self.assertRaises(Exception, self.sut.next)
        self.assertRaises(Exception, self.sut.prev)

    def test_next_will_stop_if_no_track_and_current_track_playing(self):
        track = Mock()
        track.playlist_entry = Mock()
        track.playlist_entry.next = None
        self.sut.current_track = track
        self.sut.backend = self.backend
        self.sut.next()
        self.backend.play_file.assert_not_called()
        self.backend.stop.assert_called_once()

    def test_next_will_play_next_track(self):
        track = Mock()
        next_track = Mock()
        track.playlist_entry = Mock()
        track.playlist_entry.next = Mock()
        track.playlist_entry.next.track = next_track
        self.sut.current_track = track
        self.sut.backend = self.backend
        self.sut.next()
        self.backend.play_file.assert_called_with(next_track)

    def test_prev_will_stop_if_no_track_and_current_track_playing(self):
        track = Mock()
        track.playlist_entry = Mock()
        track.playlist_entry.prev = None
        self.sut.current_track = track
        self.sut.backend = self.backend
        self.sut.prev()
        self.backend.play_file.assert_not_called()
        self.backend.stop.assert_called_once()

    def test_prev_will_play_prev_track(self):
        track = Mock()
        prev_track = Mock()
        track.playlist_entry = Mock()
        track.playlist_entry.prev = Mock()
        track.playlist_entry.prev.track = prev_track
        self.sut.current_track = track
        self.sut.backend = self.backend
        self.sut.prev()
        self.backend.play_file.assert_called_with(prev_track)

