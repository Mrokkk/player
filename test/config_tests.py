#!/usr/bin/env python3

from unittest import TestCase
from unittest.mock import Mock, MagicMock, patch
from playerlib.config import *

class ConfigTests(TestCase):

    def test_can_read_simple_config(self):
        config_mock = Mock()
        config_mock.backend = 'some_backend'
        config_mock.backend_path = '/path/to/some_backend'
        with patch('importlib.machinery.SourceFileLoader') as loader_class_mock:
            loader_mock = Mock()
            loader_mock.load_module.return_value = config_mock
            loader_class_mock.return_value = loader_mock
            sut = Config()
            self.assertEqual(sut.backend, 'some_backend')
            self.assertEqual(sut.backend_path, '/path/to/some_backend')

