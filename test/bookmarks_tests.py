#!/usr/bin/env python3

from unittest import TestCase
from unittest.mock import Mock, patch, ANY, call

class BookmarksTests(TestCase):

    def setUp(self):
        self.command_handler_mock = Mock()
        self.command_panel_mock = Mock()
        self.window_mock = Mock()
        self.app_instance = Mock()
        self.app_instance.command_handler = self.command_handler_mock
        self.app_instance.command_panel = self.command_panel_mock
        self.app_instance.window = self.window_mock
        self.app_mock = Mock()
        self.app_mock.return_value = self.app_instance
        patch('urwim.asynchronous', lambda x: x).start()
        patch('urwim.App', self.app_mock).start()
        import playerlib.bookmarks.bookmarks
        self.Bookmarks = playerlib.bookmarks.bookmarks.Bookmarks
        self.config_mock = Mock()
        self.config_mock.bookmarks_file = '/bookmarks.json'

    def test_can_start_when_bookmarks_file_does_not_exist(self):
        with patch('os.path.exists') as exists_mock:
            exists_mock.return_value = False
            sut = self.Bookmarks(self.config_mock)
            self.assertEqual(len(sut.content), 0)

    def test_can_start_when_bookmarks_file_exists(self):
        with patch('os.path.exists') as exists_mock, \
                patch('builtins.open') as open_mock, \
                patch('json.load') as json_load_mock:
            exists_mock.return_value = True
            json_load_mock.return_value = ['/path1', '/path2', '/path3']
            sut = self.Bookmarks(self.config_mock)
            self.assertEqual(len(sut.content), 3)

    def test_adding_bookmark_also_saves_file(self):
        with patch('os.path.exists') as exists_mock, \
                patch('builtins.open') as open_mock, \
                patch('json.dump') as json_dump_mock:
            exists_mock.return_value = False
            sut = self.Bookmarks(self.config_mock)
            sut.add('/path')
            open_mock.assert_called_once_with(self.config_mock.bookmarks_file, 'w')
            json_dump_mock.assert_called_once_with(['/path'], ANY)

    def test_can_go_to_selected_bookmark(self):
        with patch('os.path.exists') as exists_mock, \
                patch('builtins.open') as open_mock, \
                patch('json.dump') as json_dump_mock:
            exists_mock.return_value = False
            sut = self.Bookmarks(self.config_mock)
            sut.add('/path')
            sut.handle_input('enter')
            self.command_handler_mock.assert_has_calls([call(':change_dir /path'), call(':toggle_pane_view')])

    def test_can_go_to_bookmark_by_number(self):
        with patch('os.path.exists') as exists_mock, \
                patch('builtins.open') as open_mock, \
                patch('json.dump') as json_dump_mock:
            exists_mock.return_value = False
            sut = self.Bookmarks(self.config_mock)
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
                self.command_handler_mock.assert_has_calls([call(':change_dir /path' + str(i)), call(':toggle_pane_view')])
                self.command_handler_mock.reset_mock()

    def test_should_raise_runtime_error_if_bookmarks_number_wrong(self):
        with patch('os.path.exists') as exists_mock, \
                patch('builtins.open') as open_mock, \
                patch('json.dump') as json_dump_mock:
            exists_mock.return_value = False
            sut = self.Bookmarks(self.config_mock)
            sut.add('/path1')
            sut.handle_input('3')
            self.command_handler_mock.assert_called_once_with(':error "no such bookmark: 3"')

    def test_should_not_add_same_bookmark_twice(self):
        # TODO
        pass

