#!/usr/bin/env python3

from unittest import TestCase
from unittest.mock import Mock, MagicMock, patch
from playerlib.backends.mplayer import *

class MplayerBackendTests(TestCase):

    def setUp(self):
        self.sut = MplayerBackend(lambda: None, lambda: None)

    def test_should_raise_exception_when_no_track_given(self):
        self.assertRaises(RuntimeError, self.sut.play_track, None)

    def test_backend_should_be_started_if_no_track_playing(self):
        track = Mock()
        track.path = 'some_file.mp3'
        track.offset = 0
        with patch('subprocess.Popen') as popen_mock, \
                patch('threading.Thread') as thread_mock:
            mplayer_mock = Mock()
            popen_mock.return_value = mplayer_mock
            self.sut.play_track(track)
            popen_mock.assert_called_once()
            mplayer_mock.stdin.write.assert_not_called()

    def test_seek_command_should_be_sent_if_tracks_are_same(self):
        mplayer_mock = Mock()
        self.sut.mplayer = mplayer_mock
        track = Mock()
        track.path = 'file.mp3'
        track.offset = 20
        self.sut.current_track = track
        with patch('subprocess.Popen') as popen_mock, \
                patch('threading.Thread') as thread_mock:
            self.sut.play_track(track)
            popen_mock.assert_not_called()
            mplayer_mock.stdin.write.assert_called_once_with('seek 20 2 1\n')

    def test_loadfile_command_should_be_sent_if_track_playing_and_paths_differ(self):
        last_track = Mock()
        last_track.path = 'some_file1.mp3'
        last_track.offset = 0
        mplayer_mock = Mock()
        self.sut.current_track = last_track
        self.sut.mplayer = mplayer_mock
        track = Mock()
        track.path = 'some_file.mp3'
        track.offset = 0
        with patch('subprocess.Popen') as popen_mock, \
                patch('threading.Thread') as thread_mock:
            self.sut.play_track(track)
            popen_mock.assert_not_called()
            mplayer_mock.stdin.write.assert_called_once_with('loadfile "some_file.mp3"\n')

    def test_seek_command_should_be_sent_if_track_playing_and_paths_dont_differ(self):
        last_track = Mock()
        last_track.path = 'file.mp3'
        last_track.offset = 0
        mplayer_mock = Mock()
        self.sut.current_track = last_track
        self.sut.mplayer = mplayer_mock
        track = Mock()
        track.path = 'file.mp3'
        track.offset = 20
        with patch('subprocess.Popen') as popen_mock, \
                patch('threading.Thread') as thread_mock:
            self.sut.play_track(track)
            popen_mock.assert_not_called()
            mplayer_mock.stdin.write.assert_called_once_with('seek 20 2 1\n')

    def test_backend_should_be_started_and_seek_command_should_be_sent_if_track_has_offset(self):
        track = Mock()
        track.path = 'some_file.mp3'
        track.offset = 215
        with patch('subprocess.Popen') as popen_mock, \
                patch('threading.Thread') as thread_mock:
            mplayer_mock = Mock()
            popen_mock.return_value = mplayer_mock
            self.sut.play_track(track)
            popen_mock.assert_called_once()
            mplayer_mock.stdin.write.assert_called_once_with('seek 215 2 1\n')

    def test_stop_should_be_ignored_if_no_track_playing(self):
        mplayer_mock = Mock()
        self.sut.current_track = None
        self.sut.mplayer = mplayer_mock
        self.sut.stop()
        mplayer_mock.stdin.write.assert_not_called()

    def test_stop_should_send_command_if_track_playing(self):
        mplayer_mock = Mock()
        self.sut.current_track = Mock()
        self.sut.mplayer = mplayer_mock
        self.sut.stop()
        mplayer_mock.stdin.write.assert_called_once_with('stop\n')

    def test_toggle_pause_should_be_ignored_if_no_track_playing(self):
        mplayer_mock = Mock()
        self.sut.current_track = None
        self.sut.mplayer = mplayer_mock
        self.sut.toggle_pause()
        mplayer_mock.stdin.write.assert_not_called()

    def test_toggle_pause_should_send_command_if_track_playing(self):
        mplayer_mock = Mock()
        self.sut.current_track = Mock()
        self.sut.mplayer = mplayer_mock
        self.sut.toggle_pause()
        mplayer_mock.stdin.write.assert_called_once_with('pause\n')

    def test_can_be_closed(self):
        self.sut.mplayer = None
        self.sut.quit()

    def test_can_be_closed_if_backend_running(self):
        mplayer_mock = Mock()
        self.sut.mplayer = mplayer_mock
        self.sut.quit()
        mplayer_mock.stdin.write.assert_called_once_with('quit\n')

    def test_should_terminate_backend_if_it_doesnt_close(self):
        mplayer_mock = Mock()
        mplayer_mock.wait.side_effect = RuntimeError('')
        self.sut.mplayer = mplayer_mock
        self.sut.quit()
        mplayer_mock.stdin.write.assert_called_once_with('quit\n')
