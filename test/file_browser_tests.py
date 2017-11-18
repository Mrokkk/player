#!/usr/bin/env python3

from unittest import TestCase
from unittest.mock import Mock, patch

from playerlib.file_browser.file_browser import *

class FileBrowserTests(TestCase):

    def setUp(self):
        self.add_to_playlist_mock = Mock()
        self.error_handler_mock = Mock()

    def test_can_properly_create_current_dir_view(self):
        with patch('os.getcwd') as getcwd_mock, \
                patch('os.path.isdir') as isdir_mock, \
                patch('os.listdir') as listdir_mock:
            getcwd_mock.return_value = '/dir'
            listdir_mock.return_value = ['some_file', 'some_other_file', 'some dir', '1 - music file.mp3', '02 - sound.wav']
            isdir_mock.side_effect = [False, False, True, False, False]
            sut = FileBrowser(self.add_to_playlist_mock, self.error_handler_mock)
            self.assertEqual(len(sut.content), 5)
            self.assertEqual(sut.content[0].path(), '/dir/some dir')
            self.assertEqual(sut.content[1].path(), '/dir/1 - music file.mp3')
            self.assertEqual(sut.content[2].path(), '/dir/02 - sound.wav')
            self.assertEqual(sut.content[3].path(), '/dir/some_file')
            self.assertEqual(sut.content[4].path(), '/dir/some_other_file')
            self.error_handler_mock.assert_not_called()

    def test_can_add_to_playlist(self):
        with patch('os.getcwd') as getcwd_mock, \
                patch('os.path.isdir') as isdir_mock, \
                patch('os.listdir') as listdir_mock:
            getcwd_mock.return_value = '/dir'
            listdir_mock.return_value = ['some_file']
            isdir_mock.side_effect = [False]
            sut = FileBrowser(self.add_to_playlist_mock, self.error_handler_mock)
            sut.unhandled_input('a')
            self.add_to_playlist_mock.assert_called_once_with('/dir/some_file')
            self.error_handler_mock.assert_not_called()

    def test_add_to_playlist_calls_error_handler_when_exception_occurred(self):
        with patch('os.getcwd') as getcwd_mock, \
                patch('os.path.isdir') as isdir_mock, \
                patch('os.listdir') as listdir_mock:
            getcwd_mock.return_value = '/dir'
            listdir_mock.return_value = ['some_file']
            isdir_mock.side_effect = [False]
            self.add_to_playlist_mock.side_effect = RuntimeError('Some error')
            sut = FileBrowser(self.add_to_playlist_mock, self.error_handler_mock)
            sut.unhandled_input('a')
            self.add_to_playlist_mock.assert_called_once_with('/dir/some_file')
            self.error_handler_mock.assert_called_once_with('Some error')

