#!/usr/bin/env python3

from unittest import TestCase
from unittest.mock import Mock, MagicMock, patch
from playerlib.backends.backend_factory import *
from playerlib.backends.mplayer import *

class BackendFactoryTests(TestCase):

    def setUp(self):
        self.context_mock = Mock()
        self.context_mock.config = Mock()
        self.sut = BackendFactory(self.context_mock.config, Mock(), Mock())

    def test_can_create_mplayer_backend(self):
        self.context_mock.config.backend.name = 'mplayer'
        backend = self.sut.create()
        self.assertEqual(backend.__class__, MplayerBackend)

    def test_should_raise_exception_when_improper_backend_name(self):
        self.context_mock.config.backend.name = 'aa'
        self.assertRaises(RuntimeError, self.sut.create)

