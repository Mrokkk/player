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
                patch('os.path.exists') as exists_mock, \
                patch('os.listdir') as listdir_mock:
            getcwd_mock.return_value = '/dir'
            exists_mock.return_value = False
            listdir_mock.return_value = ['some_file', 'some_other_file', 'some dir', '1 - music file.mp3', '02 - sound.wav']
            isdir_mock.side_effect = [False, False, True, False, False]
            sut = FileBrowser(self.add_to_playlist_mock, self.error_handler_mock)
            self.assertEqual(len(sut.content), 6)
            self.assertEqual(sut.content[0].text(), '/dir')
            self.assertEqual(sut.content[1].path(), '/dir/some dir')
            self.assertEqual(sut.content[2].path(), '/dir/1 - music file.mp3')
            self.assertEqual(sut.content[3].path(), '/dir/02 - sound.wav')
            self.assertEqual(sut.content[4].path(), '/dir/some_file')
            self.assertEqual(sut.content[5].path(), '/dir/some_other_file')
            self.error_handler_mock.assert_not_called()

    def test_can_add_to_playlist(self):
        with patch('os.getcwd') as getcwd_mock, \
                patch('os.path.isdir') as isdir_mock, \
                patch('os.path.exists') as exists_mock, \
                patch('os.listdir') as listdir_mock:
            getcwd_mock.return_value = '/dir'
            exists_mock.return_value = False
            listdir_mock.return_value = ['some_file']
            isdir_mock.side_effect = [False]
            sut = FileBrowser(self.add_to_playlist_mock, self.error_handler_mock)
            sut.content.set_focus(1)
            sut.unhandled_input('a')
            self.add_to_playlist_mock.assert_called_once_with('/dir/some_file')
            self.error_handler_mock.assert_not_called()

    def test_add_to_playlist_calls_error_handler_when_exception_occurred(self):
        with patch('os.getcwd') as getcwd_mock, \
                patch('os.path.isdir') as isdir_mock, \
                patch('os.path.exists') as exists_mock, \
                patch('os.listdir') as listdir_mock:
            getcwd_mock.return_value = '/dir'
            exists_mock.return_value = False
            listdir_mock.return_value = ['some_file']
            isdir_mock.side_effect = [False]
            self.add_to_playlist_mock.side_effect = RuntimeError('Some error')
            sut = FileBrowser(self.add_to_playlist_mock, self.error_handler_mock)
            sut.content.set_focus(1)
            sut.unhandled_input('a')
            self.add_to_playlist_mock.assert_called_once_with('/dir/some_file')
            self.error_handler_mock.assert_called_once_with('Some error')

    def test_can_replace_playlist(self):
        with patch('os.getcwd') as getcwd_mock, \
                patch('os.path.isdir') as isdir_mock, \
                patch('os.path.exists') as exists_mock, \
                patch('os.listdir') as listdir_mock:
            getcwd_mock.return_value = '/dir'
            exists_mock.return_value = False
            listdir_mock.return_value = ['some_file']
            isdir_mock.side_effect = [False]
            sut = FileBrowser(self.add_to_playlist_mock, self.error_handler_mock)
            sut.content.set_focus(1)
            sut.unhandled_input('r')
            self.add_to_playlist_mock.assert_called_once_with('/dir/some_file', clear=True)
            self.error_handler_mock.assert_not_called()

    def test_replace_playlist_calls_error_handler_when_exception_occurred(self):
        with patch('os.getcwd') as getcwd_mock, \
                patch('os.path.isdir') as isdir_mock, \
                patch('os.path.exists') as exists_mock, \
                patch('os.listdir') as listdir_mock:
            getcwd_mock.return_value = '/dir'
            exists_mock.return_value = False
            listdir_mock.return_value = ['some_file']
            isdir_mock.side_effect = [False]
            self.add_to_playlist_mock.side_effect = RuntimeError('Some error')
            sut = FileBrowser(self.add_to_playlist_mock, self.error_handler_mock)
            sut.content.set_focus(1)
            sut.unhandled_input('r')
            self.add_to_playlist_mock.assert_called_once_with('/dir/some_file', clear=True)
            self.error_handler_mock.assert_called_once_with('Some error')

    def test_can_toggle_dir(self):
        with patch('os.getcwd') as getcwd_mock, \
                patch('os.path.isdir') as isdir_mock, \
                patch('os.path.exists') as exists_mock, \
                patch('os.listdir') as listdir_mock:
            getcwd_mock.return_value = '/dir'
            exists_mock.return_value = False
            listdir_mock.side_effect = [['some_file', 'some_other_file', 'some dir'], ['file in dir', 'file 2']]
            isdir_mock.side_effect = [False, False, True, True, False, False]
            sut = FileBrowser(self.add_to_playlist_mock, self.error_handler_mock)
            sut.content.set_focus(1)
            sut.unhandled_input('enter')
            self.assertEqual(len(sut.content), 6)
            self.assertEqual(sut.content[0].text(), '/dir')
            self.assertEqual(sut.content[1].path(), '/dir/some dir')
            self.assertEqual(sut.content[2].path(), '/dir/some dir/file 2')
            self.assertEqual(sut.content[3].path(), '/dir/some dir/file in dir')
            self.assertEqual(sut.content[4].path(), '/dir/some_file')
            self.assertEqual(sut.content[5].path(), '/dir/some_other_file')
            sut.unhandled_input('enter')
            self.assertEqual(len(sut.content), 4)
            self.assertEqual(sut.content[0].text(), '/dir')
            self.assertEqual(sut.content[1].path(), '/dir/some dir')
            self.assertEqual(sut.content[2].path(), '/dir/some_file')
            self.assertEqual(sut.content[3].path(), '/dir/some_other_file')

    def test_toggling_empty_dir_does_nothing(self):
        with patch('os.getcwd') as getcwd_mock, \
                patch('os.path.isdir') as isdir_mock, \
                patch('os.path.exists') as exists_mock, \
                patch('os.listdir') as listdir_mock:
            getcwd_mock.return_value = '/dir'
            exists_mock.return_value = False
            listdir_mock.side_effect = [['some_file', 'some_other_file', 'some dir'], [], []]
            isdir_mock.side_effect = [False, False, True, True, True]
            sut = FileBrowser(self.add_to_playlist_mock, self.error_handler_mock)
            sut.content.set_focus(1)
            sut.unhandled_input('enter')
            self.assertEqual(len(sut.content), 4)
            self.assertEqual(sut.content[0].text(), '/dir')
            self.assertEqual(sut.content[1].path(), '/dir/some dir')
            self.assertEqual(sut.content[2].path(), '/dir/some_file')
            self.assertEqual(sut.content[3].path(), '/dir/some_other_file')
            sut.unhandled_input('enter')
            self.assertEqual(len(sut.content), 4)
            self.assertEqual(sut.content[0].text(), '/dir')
            self.assertEqual(sut.content[1].path(), '/dir/some dir')
            self.assertEqual(sut.content[2].path(), '/dir/some_file')
            self.assertEqual(sut.content[3].path(), '/dir/some_other_file')

    def test_toggling_a_file_does_nothing(self):
        with patch('os.getcwd') as getcwd_mock, \
                patch('os.path.isdir') as isdir_mock, \
                patch('os.path.exists') as exists_mock, \
                patch('os.listdir') as listdir_mock:
            getcwd_mock.return_value = '/dir'
            exists_mock.return_value = False
            listdir_mock.side_effect = [['some_file', 'some_other_file', 'some dir'], [], []]
            isdir_mock.side_effect = [False, False, True, False, False]
            sut = FileBrowser(self.add_to_playlist_mock, self.error_handler_mock)
            sut.content.set_focus(2)
            sut.unhandled_input('enter')
            self.assertEqual(len(sut.content), 4)
            self.assertEqual(sut.content[0].text(), '/dir')
            self.assertEqual(sut.content[1].path(), '/dir/some dir')
            self.assertEqual(sut.content[2].path(), '/dir/some_file')
            self.assertEqual(sut.content[3].path(), '/dir/some_other_file')
            sut.unhandled_input('enter')
            self.assertEqual(len(sut.content), 4)
            self.assertEqual(sut.content[0].text(), '/dir')
            self.assertEqual(sut.content[1].path(), '/dir/some dir')
            self.assertEqual(sut.content[2].path(), '/dir/some_file')
            self.assertEqual(sut.content[3].path(), '/dir/some_other_file')

    def test_can_change_dir_to_selected_dir(self):
        with patch('os.getcwd') as getcwd_mock, \
                patch('os.path.isdir') as isdir_mock, \
                patch('os.path.exists') as exists_mock, \
                patch('os.listdir') as listdir_mock:
            getcwd_mock.return_value = '/dir'
            exists_mock.return_value = False
            listdir_mock.side_effect = [['some dir'], ['file in dir', 'file 2']]
            isdir_mock.side_effect = [True, True, False, False]
            sut = FileBrowser(self.add_to_playlist_mock, self.error_handler_mock)
            sut.content.set_focus(1)
            sut.unhandled_input('C')
            self.assertEqual(len(sut.content), 3)
            self.assertEqual(sut.content[0].text(), '/dir/some dir')
            self.assertEqual(sut.content[1].path(), '/dir/some dir/file 2')
            self.assertEqual(sut.content[2].path(), '/dir/some dir/file in dir')

    def test_cannot_change_dir_to_file(self):
        with patch('os.getcwd') as getcwd_mock, \
                patch('os.path.isdir') as isdir_mock, \
                patch('os.path.exists') as exists_mock, \
                patch('os.listdir') as listdir_mock:
            getcwd_mock.return_value = '/dir'
            exists_mock.return_value = False
            listdir_mock.side_effect = [['some file']]
            isdir_mock.side_effect = [False, False, False, False]
            sut = FileBrowser(self.add_to_playlist_mock, self.error_handler_mock)
            sut.content.set_focus(1)
            sut.unhandled_input('C')
            self.assertEqual(len(sut.content), 2)
            self.assertEqual(sut.content[0].text(), '/dir')
            self.assertEqual(sut.content[1].path(), '/dir/some file')
            sut.unhandled_input('C')
            self.assertEqual(len(sut.content), 2)
            self.assertEqual(sut.content[0].text(), '/dir')
            self.assertEqual(sut.content[1].path(), '/dir/some file')

    def test_can_go_up(self):
        with patch('os.getcwd') as getcwd_mock, \
                patch('os.path.isdir') as isdir_mock, \
                patch('os.path.exists') as exists_mock, \
                patch('os.listdir') as listdir_mock:
            getcwd_mock.return_value = '/dir'
            exists_mock.return_value = False
            listdir_mock.side_effect = [['some dir'], ['file']]
            isdir_mock.side_effect = [True, True, False, False]
            sut = FileBrowser(self.add_to_playlist_mock, self.error_handler_mock)
            sut.content.set_focus(1)
            sut.unhandled_input('u')
            self.assertEqual(len(sut.content), 2)
            self.assertEqual(sut.content[0].text(), '/')
            self.assertEqual(sut.content[1].path(), '/file')

    def test_go_back_restores_last_cursor_position(self):
        with patch('os.getcwd') as getcwd_mock, \
                patch('os.path.isdir') as isdir_mock, \
                patch('os.path.exists') as exists_mock, \
                patch('os.listdir') as listdir_mock:
            getcwd_mock.return_value = '/dir'
            exists_mock.return_value = False
            listdir_mock.side_effect = [['dir1', 'dir2', 'some dir'], ['file'], ['dir1', 'dir2', 'some dir']]
            isdir_mock.side_effect = [True, True, True, True, False, True, True, True, True]
            sut = FileBrowser(self.add_to_playlist_mock, self.error_handler_mock)
            sut.content.set_focus(3)
            sut.unhandled_input('C')
            self.assertEqual(len(sut.content), 2)
            self.assertEqual(sut.content.focus, 1)
            sut.unhandled_input('u')
            self.assertEqual(len(sut.content), 4)
            self.assertEqual(sut.content.focus, 3)

    def test_can_reload_dir(self):
        with patch('os.getcwd') as getcwd_mock, \
                patch('os.path.isdir') as isdir_mock, \
                patch('os.path.exists') as exists_mock, \
                patch('os.listdir') as listdir_mock:
            getcwd_mock.return_value = '/dir'
            exists_mock.return_value = False
            listdir_mock.side_effect = [['some dir'], ['file']]
            isdir_mock.side_effect = [True, True, False, False]
            sut = FileBrowser(self.add_to_playlist_mock, self.error_handler_mock)
            sut.content.set_focus(1)
            sut.unhandled_input('R')
            self.assertEqual(len(sut.content), 2)
            self.assertEqual(sut.content[1].path(), '/dir/file')

    def test_can_scroll_to_the_beginning(self):
        with patch('os.getcwd') as getcwd_mock, \
                patch('os.path.isdir') as isdir_mock, \
                patch('os.path.exists') as exists_mock, \
                patch('os.listdir') as listdir_mock:
            getcwd_mock.return_value = '/dir'
            exists_mock.return_value = False
            listdir_mock.return_value = ['some_file', 'some_other_file', 'some dir', '1 - music file.mp3', '02 - sound.wav']
            isdir_mock.side_effect = [False, False, True, False, False]
            sut = FileBrowser(self.add_to_playlist_mock, self.error_handler_mock)
            sut.content.set_focus(3)
            sut.unhandled_input('home')
            self.error_handler_mock.assert_not_called()
            self.assertEqual(sut.content.focus, 0)

    def test_can_scroll_to_the_end(self):
        with patch('os.getcwd') as getcwd_mock, \
                patch('os.path.isdir') as isdir_mock, \
                patch('os.path.exists') as exists_mock, \
                patch('os.listdir') as listdir_mock:
            getcwd_mock.return_value = '/dir'
            exists_mock.return_value = False
            listdir_mock.return_value = ['some_file', 'some_other_file', 'some dir', '1 - music file.mp3', '02 - sound.wav']
            isdir_mock.side_effect = [False, False, True, False, False]
            sut = FileBrowser(self.add_to_playlist_mock, self.error_handler_mock)
            sut.content.set_focus(1)
            sut.unhandled_input('end')
            self.error_handler_mock.assert_not_called()
            self.assertEqual(sut.content.focus, 5)

    def test_can_search_forward(self):
        with patch('os.getcwd') as getcwd_mock, \
                patch('os.path.isdir') as isdir_mock, \
                patch('os.path.exists') as exists_mock, \
                patch('os.listdir') as listdir_mock:
            getcwd_mock.return_value = '/dir'
            exists_mock.return_value = False
            listdir_mock.return_value = ['some_file', 'some_other_file', 'some dir', '1 - music file.mp3', '02 - sound.wav']
            isdir_mock.side_effect = [False, False, True, False, False]
            sut = FileBrowser(self.add_to_playlist_mock, self.error_handler_mock)
            sut.content.set_focus(1)
            # Order: 'some dir', '1 - music file.mp3', '02 - sound.wav', 'some_file', some_other_file'
            sut.search_forward('other')
            self.assertEqual(sut.content.focus, 5)
            sut.content.set_focus(1)
            sut.search_forward('some')
            self.assertEqual(sut.content.focus, 4)
            sut.search_forward('some')
            self.assertEqual(sut.content.focus, 5)
            sut.search_forward('some')
            self.assertEqual(sut.content.focus, 5)

    def test_can_search_backward(self):
        with patch('os.getcwd') as getcwd_mock, \
                patch('os.path.isdir') as isdir_mock, \
                patch('os.path.exists') as exists_mock, \
                patch('os.listdir') as listdir_mock:
            getcwd_mock.return_value = '/dir'
            exists_mock.return_value = False
            listdir_mock.return_value = ['some_file', 'some_other_file', 'some dir', '1 - music file.mp3', '02 - sound.wav']
            isdir_mock.side_effect = [False, False, True, False, False]
            sut = FileBrowser(self.add_to_playlist_mock, self.error_handler_mock)
            sut.content.set_focus(5)
            # Order: 'some dir', '1 - music file.mp3', '02 - sound.wav', 'some_file', some_other_file'
            sut.search_backward('other')
            self.assertEqual(sut.content.focus, 5)
            sut.search_backward('02')
            self.assertEqual(sut.content.focus, 3)
            sut.search_backward('sound')
            self.assertEqual(sut.content.focus, 3)
            sut.search_backward('some')
            self.assertEqual(sut.content.focus, 1)
            sut.search_backward('some')
            self.assertEqual(sut.content.focus, 1)

    def test_can_show_bookmarks_view(self):
        with patch('os.getcwd') as getcwd_mock, \
                patch('os.path.isdir') as isdir_mock, \
                patch('os.path.exists') as exists_mock, \
                patch('os.listdir') as listdir_mock:
            getcwd_mock.return_value = '/dir'
            exists_mock.return_value = False
            listdir_mock.return_value = ['some_file', 'some_other_file', 'some dir', '1 - music file.mp3', '02 - sound.wav']
            isdir_mock.side_effect = [False, False, True, False, False]
            sut = FileBrowser(self.add_to_playlist_mock, self.error_handler_mock)
            sut.unhandled_input('b')
            self.assertEqual(sut.view.original_widget, sut.bookmarks_view)
            sut.unhandled_input('b')
            self.assertEqual(sut.view.original_widget, sut.file_browser_view)

    def test_can_add_bookmark(self):
        with patch('os.getcwd') as getcwd_mock, \
                patch('os.path.isdir') as isdir_mock, \
                patch('os.listdir') as listdir_mock, \
                patch('os.path.exists') as exists_mock, \
                patch('builtins.open') as open_mock:
            getcwd_mock.return_value = '/dir'
            exists_mock.return_value = False
            listdir_mock.return_value = ['some_file', 'some_other_file', 'some dir', '1 - music file.mp3', '02 - sound.wav']
            isdir_mock.side_effect = [False, False, True, False, False]
            sut = FileBrowser(self.add_to_playlist_mock, self.error_handler_mock)
            sut.unhandled_input('B')
            self.assertEqual(len(sut.bookmarks_view.content), 2)
            self.assertEqual(sut.bookmarks_view.content[0].text(), 'Bookmarks')
            self.assertEqual(sut.bookmarks_view[1], '/dir')

    def test_cannot_add_same_bookmark_twice(self):
        pass

    def test_ignores_other_keys(self):
        with patch('os.getcwd') as getcwd_mock, \
                patch('os.path.isdir') as isdir_mock, \
                patch('os.path.exists') as exists_mock, \
                patch('os.listdir') as listdir_mock:
            getcwd_mock.return_value = '/dir'
            exists_mock.return_value = False
            listdir_mock.return_value = ['some_file']
            isdir_mock.side_effect = [False]
            sut = FileBrowser(self.add_to_playlist_mock, self.error_handler_mock)
            sut.content.set_focus(1)
            sut.unhandled_input('c')
            sut.unhandled_input('d')
            sut.unhandled_input('e')
            self.add_to_playlist_mock.assert_not_called()
            self.error_handler_mock.assert_not_called()

