#!/usr/bin/env python3

from unittest import TestCase
from unittest.mock import Mock
from playerlib.backends.backend_interface import *

class BackendInterfaceTests(TestCase):

    def test_should_raise_runtime_error_on_all_methods(self):
        sut = Backend()
        self.assertRaises(RuntimeError, sut.play_track, Mock())
        self.assertRaises(RuntimeError, sut.toggle_pause)
        self.assertRaises(RuntimeError, sut.stop)
        self.assertRaises(RuntimeError, sut.seek, Mock())
        self.assertRaises(RuntimeError, sut.seek_percentage, Mock())
        self.assertRaises(RuntimeError, sut.seek_forward, Mock())
        self.assertRaises(RuntimeError, sut.seek_backward, Mock())
        self.assertRaises(RuntimeError, sut.set_volume, Mock())
        self.assertRaises(RuntimeError, sut.quit)

