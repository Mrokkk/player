#!/usr/bin/env python3

import os
import sys
import unittest
import unittest.mock
BASE_DIR = os.path.abspath(os.path.dirname(sys.argv[0]) + '/..')
sys.path.insert(1, BASE_DIR)
from playerlib.playback_controller import *

class TestPlaybackController(unittest.TestCase):

    def setUp(self):
        self.backend = unittest.mock.Mock()
        self.backend_factory = unittest.mock.MagicMock()
        self.backend_factory.create.return_value = self.backend
        self.sut = PlaybackController(self.backend_factory)

    def test_play_will_raise_exception_when_no_track_given(self):
        self.assertRaises(RuntimeError, self.sut.play_file, None)

    def test_play_creates_backend(self):
        self.sut.play_file(unittest.mock.Mock())
        self.backend_factory.create.assert_called()
        self.assertNotEqual(self.sut.backend, None)

    def test_play_sets_current_track(self):
        self.sut.play_file(unittest.mock.Mock())
        self.assertNotEqual(self.sut.current_track, None)

    def test_play_sends_track_to_backend_and_sets_track_as_playing(self):
        track = unittest.mock.Mock()
        self.sut.play_file(track)
        self.backend.play_file.assert_called_with(track)
        track.play.assert_called()

