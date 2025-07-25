#!/usr/bin/env python3

from unittest import TestCase
from unittest.mock import Mock, patch
import playerlib.file_browser.file_browser as fb

class FileBrowserTests(TestCase):

    def setUp(self):
        self.commands_mock = Mock()
        self.FileBrowser = fb.FileBrowser

    def test_can_properly_create_current_dir_view(self):
        with patch('os.getcwd') as getcwd_mock, \
                patch('os.path.isdir') as isdir_mock, \
                patch('os.path.exists') as exists_mock, \
                patch('os.listdir') as listdir_mock:
            getcwd_mock.return_value = '/dir'
            exists_mock.return_value = False
            listdir_mock.return_value = ['some_file', 'some_other_file', 'some dir', '1 - music file.mp3', '02 - sound.wav']
            isdir_mock.side_effect = [False, False, True, False, False]
            sut = self.FileBrowser(self.commands_mock)
            self.assertEqual(len(sut.content), 5)
            self.assertEqual(sut.header.text, '/dir')
            self.assertEqual(sut.content[0].path, '/dir/some dir')
            self.assertEqual(sut.content[1].path, '/dir/1 - music file.mp3')
            self.assertEqual(sut.content[2].path, '/dir/02 - sound.wav')
            self.assertEqual(sut.content[3].path, '/dir/some_file')
            self.assertEqual(sut.content[4].path, '/dir/some_other_file')

    def test_can_add_to_playlist(self):
        with patch('os.getcwd') as getcwd_mock, \
                patch('os.path.isdir') as isdir_mock, \
                patch('os.path.exists') as exists_mock, \
                patch('os.listdir') as listdir_mock:
            getcwd_mock.return_value = '/dir'
            exists_mock.return_value = False
            listdir_mock.return_value = ['some_file']
            isdir_mock.side_effect = [False]
            sut = self.FileBrowser(self.commands_mock)
            sut.content.set_focus(0)
            sut.handle_input('a')
            self.commands_mock.add_to_playlist.assert_called_once_with('/dir/some_file')

    def test_can_replace_playlist(self):
        with patch('os.getcwd') as getcwd_mock, \
                patch('os.path.isdir') as isdir_mock, \
                patch('os.path.exists') as exists_mock, \
                patch('os.listdir') as listdir_mock:
            getcwd_mock.return_value = '/dir'
            exists_mock.return_value = False
            listdir_mock.return_value = ['some_file']
            isdir_mock.side_effect = [False]
            sut = self.FileBrowser(self.commands_mock)
            sut.content.set_focus(0)
            sut.handle_input('r')
            self.commands_mock.replace_playlist.assert_called_once_with('/dir/some_file')

    def test_can_toggle_dir(self):
        with patch('os.getcwd') as getcwd_mock, \
                patch('os.path.isdir') as isdir_mock, \
                patch('os.path.exists') as exists_mock, \
                patch('os.listdir') as listdir_mock:
            getcwd_mock.return_value = '/dir'
            exists_mock.return_value = False
            listdir_mock.side_effect = [['some_file', 'some_other_file', 'some dir'], ['file in dir', 'file 2']]
            isdir_mock.side_effect = [False, False, True, True, True, False, False]
            sut = self.FileBrowser(self.commands_mock)
            sut.content.set_focus(0)
            sut.handle_input('enter')
            self.assertEqual(len(sut.content), 5)
            self.assertEqual(sut.header.text, '/dir')
            self.assertEqual(sut.content[0].path, '/dir/some dir')
            self.assertEqual(sut.content[1].path, '/dir/some dir/file in dir')
            self.assertEqual(sut.content[2].path, '/dir/some dir/file 2')
            self.assertEqual(sut.content[3].path, '/dir/some_file')
            self.assertEqual(sut.content[4].path, '/dir/some_other_file')
            sut.handle_input('enter')
            self.assertEqual(len(sut.content), 3)
            self.assertEqual(sut.header.text, '/dir')
            self.assertEqual(sut.content[0].path, '/dir/some dir')
            self.assertEqual(sut.content[1].path, '/dir/some_file')
            self.assertEqual(sut.content[2].path, '/dir/some_other_file')

    def test_can_toggle_dir_at_the_end(self):
        with patch('os.getcwd') as getcwd_mock, \
                patch('os.path.isdir') as isdir_mock, \
                patch('os.path.exists') as exists_mock, \
                patch('os.listdir') as listdir_mock:
            getcwd_mock.return_value = '/dir'
            exists_mock.return_value = False
            listdir_mock.side_effect = [['some dir'], ['file in dir', 'file 2']]
            isdir_mock.side_effect = [True, True, False, False]
            sut = self.FileBrowser(self.commands_mock)
            sut.content.set_focus(0)
            sut.handle_input('enter')
            self.assertEqual(len(sut.content), 3)
            self.assertEqual(sut.header.text, '/dir')
            self.assertEqual(sut.content[0].path, '/dir/some dir')
            self.assertEqual(sut.content[1].path, '/dir/some dir/file 2')
            self.assertEqual(sut.content[2].path, '/dir/some dir/file in dir')
            sut.handle_input('enter')
            self.assertEqual(len(sut.content), 1)
            self.assertEqual(sut.header.text, '/dir')
            self.assertEqual(sut.content[0].path, '/dir/some dir')

    def test_toggling_empty_dir_does_nothing(self):
        with patch('os.getcwd') as getcwd_mock, \
                patch('os.path.isdir') as isdir_mock, \
                patch('os.path.exists') as exists_mock, \
                patch('os.listdir') as listdir_mock:
            getcwd_mock.return_value = '/dir'
            exists_mock.return_value = False
            listdir_mock.side_effect = [['some_file', 'some_other_file', 'some dir'], [], []]
            isdir_mock.side_effect = [False, False, True, True, True]
            sut = self.FileBrowser(self.commands_mock)
            sut.content.set_focus(0)
            sut.handle_input('enter')
            self.assertEqual(len(sut.content), 3)
            self.assertEqual(sut.header.text, '/dir')
            self.assertEqual(sut.content[0].path, '/dir/some dir')
            self.assertEqual(sut.content[1].path, '/dir/some_file')
            self.assertEqual(sut.content[2].path, '/dir/some_other_file')
            sut.handle_input('enter')
            self.assertEqual(len(sut.content), 3)
            self.assertEqual(sut.header.text, '/dir')
            self.assertEqual(sut.content[0].path, '/dir/some dir')
            self.assertEqual(sut.content[1].path, '/dir/some_file')
            self.assertEqual(sut.content[2].path, '/dir/some_other_file')

    def test_toggling_a_file_does_nothing(self):
        with patch('os.getcwd') as getcwd_mock, \
                patch('os.path.isdir') as isdir_mock, \
                patch('os.path.exists') as exists_mock, \
                patch('os.listdir') as listdir_mock:
            getcwd_mock.return_value = '/dir'
            exists_mock.return_value = False
            listdir_mock.side_effect = [['some_file', 'some_other_file', 'some dir'], [], []]
            isdir_mock.side_effect = [False, False, True, False, False]
            sut = self.FileBrowser(self.commands_mock)
            sut.content.set_focus(1)
            sut.handle_input('enter')
            self.assertEqual(len(sut.content), 3)
            self.assertEqual(sut.header.text, '/dir')
            self.assertEqual(sut.content[0].path, '/dir/some dir')
            self.assertEqual(sut.content[1].path, '/dir/some_file')
            self.assertEqual(sut.content[2].path, '/dir/some_other_file')
            sut.handle_input('enter')
            self.assertEqual(len(sut.content), 3)
            self.assertEqual(sut.header.text, '/dir')
            self.assertEqual(sut.content[0].path, '/dir/some dir')
            self.assertEqual(sut.content[1].path, '/dir/some_file')
            self.assertEqual(sut.content[2].path, '/dir/some_other_file')

    def test_can_change_dir_to_selected_dir(self):
        with patch('os.getcwd') as getcwd_mock, \
                patch('os.path.isdir') as isdir_mock, \
                patch('os.path.exists') as exists_mock, \
                patch('os.listdir') as listdir_mock:
            getcwd_mock.return_value = '/dir'
            exists_mock.return_value = False
            listdir_mock.side_effect = [['some dir'], ['file in dir', 'file 2']]
            isdir_mock.side_effect = [True, True, False, False]
            sut = self.FileBrowser(self.commands_mock)
            sut.content.set_focus(0)
            sut.handle_input('C')
            self.assertEqual(len(sut.content), 2)
            self.assertEqual(sut.header.text, '/dir/some dir')
            self.assertEqual(sut.content[0].path, '/dir/some dir/file 2')
            self.assertEqual(sut.content[1].path, '/dir/some dir/file in dir')

    def test_can_change_dir_to_empty_dir(self):
        with patch('os.getcwd') as getcwd_mock, \
                patch('os.path.isdir') as isdir_mock, \
                patch('os.path.exists') as exists_mock, \
                patch('os.listdir') as listdir_mock:
            getcwd_mock.return_value = '/dir'
            exists_mock.return_value = False
            listdir_mock.side_effect = [['some dir'], []]
            isdir_mock.side_effect = [True, True, False, False]
            sut = self.FileBrowser(self.commands_mock)
            sut.content.set_focus(0)
            sut.handle_input('C')
            self.assertEqual(len(sut.content), 0)
            self.assertEqual(sut.header.text, '/dir/some dir')

    def test_cannot_change_dir_to_file(self):
        with patch('os.getcwd') as getcwd_mock, \
                patch('os.path.isdir') as isdir_mock, \
                patch('os.path.exists') as exists_mock, \
                patch('os.listdir') as listdir_mock:
            getcwd_mock.return_value = '/dir'
            exists_mock.return_value = False
            listdir_mock.side_effect = [['some file']]
            isdir_mock.side_effect = [False, False, False, False]
            sut = self.FileBrowser(self.commands_mock)
            sut.content.set_focus(0)
            self.assertRaises(RuntimeError, sut.handle_input, 'C')
            self.assertEqual(len(sut.content), 1)
            self.assertEqual(sut.header.text, '/dir')
            self.assertEqual(sut.content[0].path, '/dir/some file')
            self.assertRaises(RuntimeError, sut.handle_input, 'C')
            self.assertEqual(len(sut.content), 1)
            self.assertEqual(sut.header.text, '/dir')
            self.assertEqual(sut.content[0].path, '/dir/some file')

    def test_can_go_up(self):
        with patch('os.getcwd') as getcwd_mock, \
                patch('os.path.isdir') as isdir_mock, \
                patch('os.path.exists') as exists_mock, \
                patch('os.listdir') as listdir_mock:
            getcwd_mock.return_value = '/dir'
            exists_mock.return_value = False
            listdir_mock.side_effect = [['some dir'], ['file']]
            isdir_mock.side_effect = [True, True, False, False]
            sut = self.FileBrowser(self.commands_mock)
            sut.content.set_focus(0)
            sut.handle_input('u')
            self.assertEqual(len(sut.content), 1)
            self.assertEqual(sut.header.text, '/')
            self.assertEqual(sut.content[0].path, '/file')

    def test_go_back_restores_last_cursor_position(self):
        with patch('os.getcwd') as getcwd_mock, \
                patch('os.path.isdir') as isdir_mock, \
                patch('os.path.exists') as exists_mock, \
                patch('os.listdir') as listdir_mock:
            getcwd_mock.return_value = '/dir'
            exists_mock.return_value = False
            listdir_mock.side_effect = [['dir1', 'dir2', 'some dir'], ['file'], ['dir1', 'dir2', 'some dir']]
            isdir_mock.side_effect = [True, True, True, True, False, True, True, True, True]
            sut = self.FileBrowser(self.commands_mock)
            sut.content.set_focus(1)
            sut.handle_input('C')
            self.assertEqual(len(sut.content), 1)
            self.assertEqual(sut.content.focus, 0)
            sut.handle_input('u')
            self.assertEqual(len(sut.content), 3)
            self.assertEqual(sut.content.focus, 1)

    def test_can_reload_dir(self):
        with patch('os.getcwd') as getcwd_mock, \
                patch('os.path.isdir') as isdir_mock, \
                patch('os.path.exists') as exists_mock, \
                patch('os.listdir') as listdir_mock:
            getcwd_mock.return_value = '/dir'
            exists_mock.return_value = False
            listdir_mock.side_effect = [['some dir'], ['file']]
            isdir_mock.side_effect = [True, True, False, False]
            sut = self.FileBrowser(self.commands_mock)
            sut.content.set_focus(0)
            sut.handle_input('R')
            self.assertEqual(len(sut.content), 1)
            self.assertEqual(sut.content[0].path, '/dir/file')

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
            sut = self.FileBrowser(self.commands_mock)
            sut.handle_input('B')
            self.commands_mock.add_bookmark.assert_called_once_with('/dir')

    def test_ignores_other_keys(self):
        with patch('os.getcwd') as getcwd_mock, \
                patch('os.path.isdir') as isdir_mock, \
                patch('os.path.exists') as exists_mock, \
                patch('os.listdir') as listdir_mock:
            getcwd_mock.return_value = '/dir'
            exists_mock.return_value = False
            listdir_mock.return_value = ['some_file']
            isdir_mock.side_effect = [False]
            sut = self.FileBrowser(self.commands_mock)
            sut.content.set_focus(0)
            sut.handle_input('c')
            sut.handle_input('d')
            sut.handle_input('e')
            self.commands_mock.assert_not_called()

    def test_is_searchable(self):
        with patch('os.getcwd') as getcwd_mock, \
                patch('os.path.isdir') as isdir_mock, \
                patch('os.path.exists') as exists_mock, \
                patch('os.listdir') as listdir_mock:
            getcwd_mock.return_value = '/dir'
            exists_mock.return_value = False
            listdir_mock.return_value = ['some_file']
            isdir_mock.side_effect = [False]
            sut = self.FileBrowser(self.commands_mock)
            self.assertTrue(hasattr(sut, 'searchable_list'))
            self.assertTrue(sut.searchable_list != None)

