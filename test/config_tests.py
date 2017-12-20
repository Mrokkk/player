#!/usr/bin/env python3

from unittest import TestCase
from unittest.mock import Mock, MagicMock, patch
from playerlib.config import *

class ConfigTests(TestCase):

    def test_can_read_simple_config(self):
        config = {
            'backend': {
                'name': 'some_backend',
                'path': '/path/to/some_backend'
            }
        }
        with patch('builtins.open') as open_mock, patch('yaml.load') as yaml_load_mock:
            yaml_load_mock.return_value = config
            sut = Config()
            open_mock.assert_called_once()
            yaml_load_mock.assert_called_once()
            self.assertEqual(sut.backend, 'some_backend')
            self.assertEqual(sut.backend_path, '/path/to/some_backend')

    def test_have_default_configuration_when_no_config_yml(self):
        with patch('builtins.open') as open_mock, patch('yaml.load') as yaml_load_mock:
            open_mock.side_effect = RuntimeError
            sut = Config()
            open_mock.assert_called_once()
            yaml_load_mock.assert_not_called()
            self.assertEqual(sut.backend, 'mplayer')
            self.assertEqual(sut.backend_path, '/usr/bin/mplayer')

