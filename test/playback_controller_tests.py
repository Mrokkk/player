#!/usr/bin/env python3

import os
import sys
from unittest import TestCase
from unittest.mock import Mock, MagicMock
BASE_DIR = os.path.abspath(os.path.dirname(sys.argv[0]) + '/..')
sys.path.insert(1, BASE_DIR)

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

    def test_play_sends_track_to_backend_and_sets_track_as_playing(self):
        track = Mock()
        self.sut.play_file(track)
        self.backend.play_file.assert_called_with(track)
        track.play.assert_called()

    def test_play_will_stop_current_track_if_exists(self):
        track = Mock()
        last_track = MagicMock()
        self.sut.current_track = last_track
        self.sut.play_file(track)
        last_track.stop.assert_called_once()

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
        track.stop.assert_called_once()
        self.assertEqual(self.sut.current_track, None)

    def test_pause_will_raise_exception_when_no_track_playing(self):
        self.assertRaises(RuntimeError, self.sut.pause)

    def test_pause_calls_toggle_pause(self):
        track = Mock()
        self.sut.current_track = track
        self.sut.backend = self.backend
        self.sut.pause()
        self.backend.toggle_pause.assert_called_once()
        track.toggle_pause.assert_called_once()
        self.assertNotEqual(self.sut.current_track, None)

