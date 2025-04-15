#!/usr/bin/env python3

from unittest import TestCase
from unittest.mock import Mock, MagicMock, patch, mock_open
from cueparser.cueparser import *

class CueParserTests(TestCase):

    def setUp(self):
        self.sut = CueParser()

    def test_can_parse_simple_album_data(self):
        lines = ['REM GENRE Heavy Metal', 'PERFORMER "Iron Maiden"', 'TITLE "The Number of the Beast"', 'FILE "album.flac" WAVE']
        m = mock_open(read_data='\n'.join(lines))
        m.return_value.__iter__ = lambda self: self
        m.return_value.__next__ = lambda self: next(iter(self.readline, ''))
        with patch('builtins.open', m):
            cuesheet = self.sut.parse('some/path')
        self.assertEqual(cuesheet.title, 'The Number of the Beast')
        self.assertEqual(cuesheet.performer, 'Iron Maiden')
        self.assertEqual(cuesheet.rem, ['GENRE Heavy Metal'])

    def test_can_parse_tracks(self):
        lines = ['FILE "album.flac" WAVE', '  TRACK 01 AUDIO', '    TITLE "Invaders"', '    PERFORMER "Iron Maiden"', '    INDEX 01 00:00:00',
                 '  TRACK 02 AUDIO', '    TITLE "Children of the Damned"', '    PERFORMER "Iron Maiden"', '    INDEX 01 03:23:00']
        m = mock_open(read_data='\n'.join(lines))
        m.return_value.__iter__ = lambda self: self
        m.return_value.__next__ = lambda self: next(iter(self.readline, ''))
        with patch('builtins.open', m):
            cuesheet = self.sut.parse('path')
        self.assertEqual(len(cuesheet.tracks), 2)
        track1 = cuesheet.tracks[0]
        track2 = cuesheet.tracks[1]
        self.assertEqual(track1.file, 'album.flac')
        self.assertEqual(track1.index, 1)
        self.assertEqual(track1.title, 'Invaders')
        self.assertEqual(track1.performer, 'Iron Maiden')
        self.assertEqual(track1.offset, 0)
        self.assertEqual(track2.file, 'album.flac')
        self.assertEqual(track2.index, 2)
        self.assertEqual(track2.title, 'Children of the Damned')
        self.assertEqual(track2.performer, 'Iron Maiden')
        self.assertEqual(track2.offset, 203)

    def test_should_ignore_track_tags_if_no_track_given(self):
        lines = ['    TITLE "Invaders"', '    PERFORMER "Iron Maiden"', '    INDEX 01 00:00:00',
                 '    TITLE "Children of the Damned"', '    PERFORMER "Iron Maiden"', '    INDEX 01 03:23:00']
        m = mock_open(read_data='\n'.join(lines))
        m.return_value.__iter__ = lambda self: self
        m.return_value.__next__ = lambda self: next(iter(self.readline, ''))
        with patch('builtins.open', m):
            cuesheet = self.sut.parse('path')
        self.assertEqual(len(cuesheet.tracks), 0)

    def test_should_ignore_trailing_whitespaces(self):
        lines = ['REM GENRE Heavy Metal  ', 'PERFORMER "Iron Maiden"   ', 'TITLE "The Number of the Beast"  \t', 'FILE "album.flac" WAVE      ']
        m = mock_open(read_data='\n'.join(lines))
        m.return_value.__iter__ = lambda self: self
        m.return_value.__next__ = lambda self: next(iter(self.readline, ''))
        with patch('builtins.open', m):
            cuesheet = self.sut.parse('path')
        self.assertEqual(cuesheet.title, 'The Number of the Beast')
        self.assertEqual(cuesheet.performer, 'Iron Maiden')
        self.assertEqual(cuesheet.rem, ['GENRE Heavy Metal'])

    def test_can_read_tracks_length(self):
        lines = ['  TRACK 01 AUDIO', '    INDEX 01 00:00:00',
                 '  TRACK 02 AUDIO', '    INDEX 01 03:23:00',
                 '  TRACK 03 AUDIO', '    INDEX 01 05:24:00']
        m = mock_open(read_data='\n'.join(lines))
        m.return_value.__iter__ = lambda self: self
        m.return_value.__next__ = lambda self: next(iter(self.readline, ''))
        with patch('builtins.open', m):
            cuesheet = self.sut.parse('path')
        self.assertEqual(len(cuesheet.tracks), 3)
        track1 = cuesheet.tracks[0]
        track2 = cuesheet.tracks[1]
        track3 = cuesheet.tracks[2]
        self.assertEqual(track1.length, 203)
        self.assertEqual(track2.length, 121)
        self.assertEqual(track3.length, 0)

    def test_supports_multiple_tracks_in_multiple_files(self):
        lines = ['FILE "file1.ape"', '  TRACK 01 AUDIO', '    INDEX 01 00:00:00',
                 '  TRACK 02 AUDIO', '    INDEX 01 03:23:00',
                 'FILE "file2.ape"', '  TRACK 03 AUDIO', '    INDEX 01 00:00:00']
        m = mock_open(read_data='\n'.join(lines))
        m.return_value.__iter__ = lambda self: self
        m.return_value.__next__ = lambda self: next(iter(self.readline, ''))
        with patch('builtins.open', m):
            cuesheet = self.sut.parse('path')
        self.assertEqual(len(cuesheet.tracks), 3)
        track1 = cuesheet.tracks[0]
        track2 = cuesheet.tracks[1]
        track3 = cuesheet.tracks[2]
        self.assertEqual(track1.file, 'file1.ape')
        self.assertEqual(track1.offset, 0)
        self.assertEqual(track1.length, 203)
        self.assertEqual(track2.file, 'file1.ape')
        self.assertEqual(track2.offset, 203)
        self.assertEqual(track2.length, 0)
        self.assertEqual(track3.file, 'file2.ape')
        self.assertEqual(track3.offset, 0)
        self.assertEqual(track3.length, 0)

    def test_supports_multiple_tracks_in_multiple_files_with_taglib(self):
        lines = ['FILE "file1.ape"', '  TRACK 01 AUDIO', '    INDEX 01 00:00:00',
                 '  TRACK 02 AUDIO', '    INDEX 01 03:23:00',
                 'FILE "file2.ape"', '  TRACK 03 AUDIO', '    INDEX 01 00:00:00']
        m = mock_open(read_data='\n'.join(lines))
        m.return_value.__iter__ = lambda self: self
        m.return_value.__next__ = lambda self: next(iter(self.readline, ''))
        with patch('taglib.File') as taglib_mock, patch('builtins.open', m):
            file1, file2 = Mock(), Mock()
            file1.length = 300
            file2.length = 400
            taglib_mock.side_effect = [file1, file2]
            cuesheet = self.sut.parse('/path', use_taglib=True)
        self.assertEqual(len(cuesheet.tracks), 3)
        track1 = cuesheet.tracks[0]
        track2 = cuesheet.tracks[1]
        track3 = cuesheet.tracks[2]
        self.assertEqual(track1.file, 'file1.ape')
        self.assertEqual(track1.offset, 0)
        self.assertEqual(track1.length, 203)
        self.assertEqual(track2.file, 'file1.ape')
        self.assertEqual(track2.offset, 203)
        self.assertEqual(track2.length, 97)
        self.assertEqual(track3.file, 'file2.ape')
        self.assertEqual(track3.offset, 0)
        self.assertEqual(track3.length, 400)

