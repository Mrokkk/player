#!/usr/bin/env python3

from unittest import TestCase
from unittest.mock import Mock, MagicMock, patch
from playerlib.tracks_factory import *

class TracksFactoryTests(TestCase):

    def setUp(self):
        self.sut = TracksFactory()

    def _prepare_tagfile(self, taglib_file_mock, nr_of_tracks):
        tracks = []
        for i in range(0, nr_of_tracks):
            t = Mock()
            t.tags = {}
            t.length = 0
            tracks.append(t)
        taglib_file_mock.side_effect = tracks

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
            self.assertEqual(tracks[0].title, 'some_file.flac')
            self.assertEqual(tracks[0].artist, None)
            self.assertEqual(tracks[0].index, '1')
            self.assertEqual(tracks[0].length, 22)
        with patch('os.path.isfile') as isfile_mock, patch('taglib.File') as taglib_file_mock:
            isfile_mock.return_value = True
            track_tags = Mock()
            track_tags.tags = {'ARTIST': ['Some Artist']}
            track_tags.length = 22
            taglib_file_mock.return_value = track_tags
            tracks = self.sut.get('some_file.flac')
            self.assertEqual(len(tracks), 1)
            self.assertEqual(tracks[0].path, 'some_file.flac')
            self.assertEqual(tracks[0].title, 'some_file.flac')
            self.assertEqual(tracks[0].artist, 'Some Artist')
            self.assertEqual(tracks[0].index, 0)
            self.assertEqual(tracks[0].length, 22)

    def test_can_handle_dir_with_music_files(self):
        with patch('os.path.isfile') as isfile_mock, \
                patch('os.path.isdir') as isdir_mock, \
                patch('os.listdir') as listdir_mock, \
                patch('taglib.File') as taglib_file_mock:
            isfile_mock.return_value = True
            isfile_mock.side_effect = [False, True, True]
            self._prepare_tagfile(taglib_file_mock, 4)
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
            isfile_mock.side_effect = [False, True, True, True, True]
            self._prepare_tagfile(taglib_file_mock, 4)
            listdir_mock.return_value = ['03 - some_file.mp3', '2 - some_other_file.mp3', '1 - some_file.mp3', 'some music.mp3']
            tracks = self.sut.get('some_dir')
            self.assertEqual(len(tracks), 4)
            self.assertEqual(tracks[0].path, 'some_dir/1 - some_file.mp3')
            self.assertEqual(tracks[1].path, 'some_dir/2 - some_other_file.mp3')
            self.assertEqual(tracks[2].path, 'some_dir/03 - some_file.mp3')
            self.assertEqual(tracks[3].path, 'some_dir/some music.mp3')

    def test_can_handle_dir_with_empty_cue_sheet(self):
        with patch('os.path.isdir') as isdir_mock, \
                patch('os.listdir') as listdir_mock, \
                patch('playerlib.tracks_factory.CueParser') as cueparser_class_mock, \
                patch('builtins.open') as open_mock:
            isdir_mock.return_value = True
            listdir_mock.return_value = ['some_sheet.cue']
            cuesheet_mock = Mock()
            cuesheet_mock.tracks = []
            cueparser_mock = Mock()
            cueparser_mock.parse.return_value = cuesheet_mock
            cueparser_class_mock.return_value = cueparser_mock
            tracks = self.sut.get('some_dir')
            self.assertEqual(len(tracks), 0)

    def test_can_handle_cuesheet(self):
        with patch('os.path.isdir') as isdir_mock, \
                patch('os.path.isfile') as isfile_mock, \
                patch('playerlib.tracks_factory.CueParser') as cueparser_class_mock, \
                patch('builtins.open') as open_mock:
            isdir_mock.return_value = False
            isfile_mock.return_value = True
            track = Mock()
            track.file = 'some_file.flac'
            track.title = ['Title']
            track.index = 1
            track.length = 203
            track.offset = 0
            cuesheet_mock = Mock()
            cuesheet_mock.title = ['Album Title']
            cuesheet_mock.tracks = [track]
            cueparser_mock = Mock()
            cueparser_mock.parse.return_value = cuesheet_mock
            cueparser_class_mock.return_value = cueparser_mock
            tracks = self.sut.get('some_cue.cue')
            self.assertEqual(len(tracks), 1)
            self.assertEqual(tracks[0].path, 'some_file.flac')
            self.assertEqual(tracks[0].title, 'Title')
            self.assertEqual(tracks[0].index, '1')
            self.assertEqual(tracks[0].length, 203)
            self.assertEqual(tracks[0].offset, 0)

    def test_can_handle_empty_cdaudio(self):
        import sys
        discid_device_mock = Mock()
        discid_read = Mock()
        discid_mock = Mock()
        discid_mock.get_default_device = discid_device_mock
        discid_mock.read = discid_read
        sys.modules['discid'] = discid_mock
        disc_mock = Mock()
        disc_mock.tracks = []
        discid_read.return_value = disc_mock
        tracks = self.sut.get('cdda://')
        self.assertEqual(len(tracks), 0)

    def test_can_handle_nonempty_cdaudio(self):
        import sys
        discid_device_mock = Mock()
        discid_read = Mock()
        discid_mock = Mock()
        discid_mock.get_default_device = discid_device_mock
        discid_mock.read = discid_read
        sys.modules['discid'] = discid_mock
        track1, track2 = Mock(), Mock()
        track1.number = 1
        track1.seconds = 53
        track2.number = 2
        track2.seconds = 218
        disc_mock = Mock()
        disc_mock.tracks = [track1, track2]
        discid_read.return_value = disc_mock
        tracks = self.sut.get('cdda://')
        self.assertEqual(len(tracks), 2)
        self.assertEqual(tracks[0].path, 'cdda://')
        self.assertEqual(tracks[0].index, 1)
        self.assertEqual(tracks[0].length, 53)
        self.assertEqual(tracks[0].offset, 0)
        self.assertEqual(tracks[1].path, 'cdda://')
        self.assertEqual(tracks[1].index, 2)
        self.assertEqual(tracks[1].length, 218)
        self.assertEqual(tracks[1].offset, 53)

    def test_should_return_none_if_path_is_neither_dir_nor_file(self):
        with patch('os.path.isfile') as isfile_mock, \
                patch('os.path.isdir') as isdir_mock:
            isfile_mock.return_value = False
            isdir_mock.return_value = False
            tracks = self.sut.get('some_path')
            self.assertEqual(tracks, None)

