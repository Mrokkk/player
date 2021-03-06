#!/usr/bin/env python3

from unittest import TestCase
from unittest.mock import Mock, patch, ANY, call

class BookmarksTests(TestCase):

    def setUp(self):
        self.commands_mock = Mock()
        patch('urwim.asynchronous', lambda x: x).start()
        import playerlib.bookmarks.bookmarks
        self.Bookmarks = playerlib.bookmarks.bookmarks.Bookmarks
        self.config_mock = Mock()
        self.config_mock.bookmarks.path = '/bookmarks.json'

    def test_can_start_when_bookmarks_file_does_not_exist(self):
        with patch('os.path.exists') as exists_mock:
            exists_mock.return_value = False
            sut = self.Bookmarks(self.config_mock, self.commands_mock)
            self.assertEqual(len(sut.content), 0)

    def test_can_start_when_bookmarks_file_exists(self):
        with patch('os.path.exists') as exists_mock, \
                patch('builtins.open') as open_mock, \
                patch('json.load') as json_load_mock:
            exists_mock.return_value = True
            json_load_mock.return_value = ['/path1', '/path2', '/path3']
            sut = self.Bookmarks(self.config_mock, self.commands_mock)
            self.assertEqual(len(sut.content), 3)

    def test_adding_bookmark_also_saves_file(self):
        with patch('os.path.exists') as exists_mock, \
                patch('builtins.open') as open_mock, \
                patch('json.dump') as json_dump_mock:
            exists_mock.return_value = False
            sut = self.Bookmarks(self.config_mock, self.commands_mock)
            sut.add('/path')
            open_mock.assert_called_once_with(self.config_mock.bookmarks.path, 'w')
            json_dump_mock.assert_called_once_with(['/path'], ANY)

    def test_can_go_to_selected_bookmark(self):
        with patch('os.path.exists') as exists_mock, \
                patch('builtins.open') as open_mock, \
                patch('json.dump') as json_dump_mock:
            exists_mock.return_value = False
            sut = self.Bookmarks(self.config_mock, self.commands_mock)
            sut.add('/path')
            sut.handle_input('enter')
            self.commands_mock.change_dir.assert_called_once_with('/path')
            self.commands_mock.toggle_pane_view.assert_called_once()

    def test_can_go_to_bookmark_by_number(self):
        with patch('os.path.exists') as exists_mock, \
                patch('builtins.open') as open_mock, \
                patch('json.dump') as json_dump_mock:
            exists_mock.return_value = False
            sut = self.Bookmarks(self.config_mock, self.commands_mock)
            sut.add('/path1')
            sut.add('/path2')
            sut.add('/path3')
            sut.add('/path4')
            sut.add('/path5')
            sut.add('/path6')
            sut.add('/path7')
            sut.add('/path8')
            sut.add('/path9')
            sut.add('/path0')
            for i in range(0, 10):
                sut.handle_input(str(i))
                self.commands_mock.change_dir.assert_called_once_with('/path' + str(i))
                self.commands_mock.toggle_pane_view.assert_called_once()
                self.commands_mock.change_dir.reset_mock()
                self.commands_mock.toggle_pane_view.reset_mock()

    def test_should_raise_runtime_error_if_bookmarks_number_wrong(self):
        with patch('os.path.exists') as exists_mock, \
                patch('builtins.open') as open_mock, \
                patch('json.dump') as json_dump_mock:
            exists_mock.return_value = False
            sut = self.Bookmarks(self.config_mock, self.commands_mock)
            sut.add('/path1')
            sut.handle_input('3')
            self.commands_mock.error.assert_called_once_with('no such bookmark: 3')

    def test_should_not_add_same_bookmark_twice(self):
        # TODO
        pass

