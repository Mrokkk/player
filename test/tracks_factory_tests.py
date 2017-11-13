#!/usr/bin/env python3

from unittest import TestCase
from unittest.mock import Mock, MagicMock, patch
from playerlib.tracks_factory import *

class TestTracksFactory(TestCase):

    def setUp(self):
        self.sut = TracksFactory()

    def test_can_handle_non_music_file(self):
        with patch('os.path.isfile') as isfile_mock, patch('taglib.File') as taglib_file_mock:
            tracks = self.sut.get('some_file')
            self.assertEqual(tracks, None)

    def test_can_handle_music_file_with_full_tags(self):
        with patch('os.path.isfile') as isfile_mock, patch('taglib.File') as taglib_file_mock:
            isfile_mock.return_value = True
            track_tags = Mock()
            track_tags.tags = {'TITLE': ['some title'], 'ARTIST': ['some artist'], 'TRACKNUMBER': ['1']}
            track_tags.length = 22
            taglib_file_mock.return_value = track_tags
            tracks = self.sut.get('some_file.mp3')
            self.assertEqual(len(tracks), 1)
            self.assertEqual(tracks[0].path, 'some_file.mp3')
            self.assertEqual(tracks[0].title, 'some title')
            self.assertEqual(tracks[0].artist, 'some artist')
            self.assertEqual(tracks[0].index, '1')
            self.assertEqual(tracks[0].length, 22)

    def test_can_handle_music_file_with_partial_tags(self):
        with patch('os.path.isfile') as isfile_mock, patch('taglib.File') as taglib_file_mock:
            isfile_mock.return_value = True
            track_tags = Mock()
            track_tags.tags = {'TRACKNUMBER': ['1']}
            track_tags.length = 22
            taglib_file_mock.return_value = track_tags
            tracks = self.sut.get('some_file.flac')
            self.assertEqual(len(tracks), 1)
            self.assertEqual(tracks[0].path, 'some_file.flac')
            self.assertEqual(tracks[0].title, None)
            self.assertEqual(tracks[0].artist, None)
            self.assertEqual(tracks[0].index, '1')
            self.assertEqual(tracks[0].length, 22)

    def test_can_handle_dir_with_music_files(self):
        with patch('os.path.isfile') as isfile_mock, \
                patch('os.path.isdir') as isdir_mock, \
                patch('os.listdir') as listdir_mock, \
                patch('taglib.File') as taglib_file_mock:
            isfile_mock.return_value = True
            isfile_mock.side_effect = [False, True, True]
            listdir_mock.return_value = ['some_file.mp3', 'some_other_file.mp3']
            tracks = self.sut.get('some_dir')
            self.assertEqual(len(tracks), 2)
            self.assertEqual(tracks[0].path, 'some_dir/some_file.mp3')
            self.assertEqual(tracks[1].path, 'some_dir/some_other_file.mp3')

    def test_tracks_have_proper_order(self):
        with patch('os.path.isfile') as isfile_mock, \
                patch('os.path.isdir') as isdir_mock, \
                patch('os.listdir') as listdir_mock, \
                patch('taglib.File') as taglib_file_mock:
            isfile_mock.return_value = True
            isfile_mock.side_effect = [False, True, True, True]
            listdir_mock.return_value = ['03 - some_file.mp3', '2 - some_other_file.mp3', '1 - some_file.mp3']
            tracks = self.sut.get('some_dir')
            self.assertEqual(len(tracks), 3)
            self.assertEqual(tracks[0].path, 'some_dir/1 - some_file.mp3')
            self.assertEqual(tracks[1].path, 'some_dir/2 - some_other_file.mp3')
            self.assertEqual(tracks[2].path, 'some_dir/03 - some_file.mp3')

    def test_can_handle_dir_with_empty_cue_sheet(self):
        with patch('os.path.isdir') as isdir_mock, \
                patch('os.listdir') as listdir_mock, \
                patch('cueparser.CueSheet') as cue_sheet_mock, \
                patch('builtins.open') as open_mock:
            isdir_mock.return_value = True
            listdir_mock.return_value = ['some_sheet.cue']
            cue_mock = Mock()
            cue_sheet_mock.return_value = cue_mock
            cue_mock.tracks = []
            tracks = self.sut.get('some_dir')
            self.assertEqual(len(tracks), 0)

    def test_can_handle_empty_cdaudio(self):
        with patch('discid.get_default_device') as discid_device_mock, \
                patch('discid.read') as discid_read:
            disc_mock = Mock()
            disc_mock.tracks = []
            discid_read.return_value = disc_mock
            tracks = self.sut.get('cdda://')
            self.assertEqual(len(tracks), 0)

