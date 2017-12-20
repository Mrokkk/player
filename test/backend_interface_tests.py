#!/usr/bin/env python3

from unittest import TestCase
from unittest.mock import Mock
from playerlib.backends.backend_interface import *

class BackendInterfaceTests(TestCase):

    def test_should_raise_runtime_error_on_all_methods(self):
        sut = Backend()
        self.assertRaises(NotImplementedError, sut.play_track, Mock())
        self.assertRaises(NotImplementedError, sut.toggle_pause)
        self.assertRaises(NotImplementedError, sut.stop)
        self.assertRaises(NotImplementedError, sut.seek, Mock())
        self.assertRaises(NotImplementedError, sut.seek_percentage, Mock())
        self.assertRaises(NotImplementedError, sut.seek_forward, Mock())
        self.assertRaises(NotImplementedError, sut.seek_backward, Mock())
        self.assertRaises(NotImplementedError, sut.set_volume, Mock())
        self.assertRaises(NotImplementedError, sut.quit)

