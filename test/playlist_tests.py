#!/usr/bin/env python3

from unittest import TestCase
from unittest.mock import Mock, patch
from playerlib.playlist.playlist import *

class PlaylistTests(TestCase):

    def setUp(self):
        self.play_callback_mock = Mock()
        self.error_handler_mock = Mock()
        self.tracks_factory_mock = Mock()
        self.sut = Playlist(self.play_callback_mock, self.error_handler_mock)
        self.sut.tracks_factory = self.tracks_factory_mock

    def _create_track(self, title=None, artist=None, index=0, length=0):
        track = Mock()
        track.title = title
        track.artist = artist
        track.index = index
        track.length = length
        track.path = '/some_path'
        return track

    def test_enter_keypress_should_fail_when_no_tracks_on_playlist(self):
        self.assertRaises(Exception, self.sut.handle_input, 'enter')
        self.play_callback_mock.assert_not_called()

    def test_enter_keypress_should_call_play_callback_if_track_is_selected(self):
        playlist_entry_mock = Mock()
        playlist_entry_mock.track = Mock()
        self.sut.content.append(playlist_entry_mock)
        self.sut.handle_input('enter')
        self.error_handler_mock.assert_not_called()
        self.play_callback_mock.assert_called_once_with(playlist_entry_mock.track)

    def test_other_keypresses_should_be_ignored(self):
        for key in ('a', 'b', 'c', 'd', 'e', ' ', ':'):
            self.sut.handle_input(key)
            self.error_handler_mock.assert_not_called()
            self.play_callback_mock.assert_not_called()

    def test_should_be_able_to_add_tracks_to_playlist(self):
        track = self._create_track()
        self.tracks_factory_mock.get.return_value = [track]
        self.sut.add_to_playlist('some_path')
        self.assertEqual(len(self.sut.content), 1)
        self.tracks_factory_mock.get.return_value = [track, track]
        self.sut.add_to_playlist('some_path')
        self.assertEqual(len(self.sut.content), 3)

    def test_should_properly_handle_track_without_title(self):
        track = self._create_track(title=None)
        self.tracks_factory_mock.get.return_value = [track]
        self.sut.add_to_playlist('some_path')
        self.assertEqual(len(self.sut.content), 1)
        self.assertEqual(self.sut.content[0].line, 'some_path 00:00:00')

    def test_should_properly_handle_track_with_title(self):
        track = self._create_track(title='some title')
        self.tracks_factory_mock.get.return_value = [track]
        self.sut.add_to_playlist('some_path')
        self.assertEqual(len(self.sut.content), 1)
        self.assertEqual(self.sut.content[0].line, '?. ? - some title 00:00:00')

    def test_should_raise_exception_if_no_tracks_from_tracks_factory(self):
        self.tracks_factory_mock.get.return_value = []
        self.assertRaises(Exception, self.sut.add_to_playlist, 'some_path')

    def test_can_clear_playlist(self):
        track = self._create_track(title='some title')
        self.tracks_factory_mock.get.return_value = [track, track, track]
        self.sut.add_to_playlist('some_path')
        self.sut.clear()
        self.assertEqual(len(self.sut.content), 0)
        self.error_handler_mock.assert_not_called()

    def test_can_replace_playlist(self):
        track = self._create_track(title='some title')
        self.tracks_factory_mock.get.return_value = [track, track, track]
        self.sut.add_to_playlist('some_path')
        track2 = self._create_track(title='some other title')
        self.tracks_factory_mock.get.return_value = [track2, track2]
        self.sut.add_to_playlist('some_path', clear=True)
        self.assertEqual(len(self.sut.content), 2)
        self.assertEqual(self.sut.content[0].track, track2)
        self.assertEqual(self.sut.content[1].track, track2)
        self.error_handler_mock.assert_not_called()

    def test_can_save_playlist(self):
        track = self._create_track(title='some title')
        self.tracks_factory_mock.get.return_value = [track]
        self.sut.add_to_playlist('some_path')
        track.to_dict.return_value = {'title:' 'some title'}
        with patch('builtins.open') as open_mock, \
                patch('json.dump') as json_dump_mock:
            self.sut.save_playlist('some_filename')
            args, kwargs = json_dump_mock.call_args
            self.assertEqual(args[0], [{'title:' 'some title'}])

    def test_can_load_playlist(self):
        with patch('builtins.open') as open_mock, \
                patch('json.load') as json_load_mock:
            json_load_mock.return_value = [{'title': 'some title'}]
            self.sut.load_playlist('some_filename')
            self.assertEqual(len(self.sut.content), 1)
            self.assertEqual(self.sut.content[0].track.title, 'some title')

