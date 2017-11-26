#!/usr/bin/env python3

from unittest import TestCase
from unittest.mock import Mock, patch, ANY

from playerlib.bookmarks.bookmarks import *

class BookmarksTests(TestCase):

    def setUp(self):
        self.config_mock = Mock()
        self.config_mock.bookmarks_file = '/bookmarks.json'
        self.command_handler_mock = Mock()

    def test_can_start_when_no_bookmarks_file(self):
        with patch('os.path.exists') as exists_mock:
            exists_mock.return_value = False
            sut = Bookmarks(self.config_mock, self.command_handler_mock)
            self.assertEqual(len(sut.content), 0)

    def test_adding_bookmark_also_saves_file(self):
        with patch('os.path.exists') as exists_mock, \
                patch('builtins.open') as open_mock, \
                patch('json.dump') as json_dump_mock:
            exists_mock.return_value = False
            sut = Bookmarks(self.config_mock, self.command_handler_mock)
            sut.add('/path')
            open_mock.assert_called_once_with(self.config_mock.bookmarks_file, 'w')
            json_dump_mock.assert_called_once_with(['/path'], ANY)

    def test_can_go_to_bookmarks(self):
        # TODO
        pass

