#!/usr/bin/env python3

from unittest import TestCase
from unittest.mock import Mock, MagicMock, patch
from playerlib.backends.mplayer.backend import Backend as MplayerBackend
from playerlib.backends.mplayer.arguments_builder import *

class MplayerBackendTests(TestCase):

    def setUp(self):
        self.sut = MplayerBackend(lambda: None, lambda: None, Mock())

    def test_should_raise_exception_when_no_track_given(self):
        self.assertRaises(RuntimeError, self.sut.play_track, None)

    def test_backend_should_be_started_if_no_track_playing(self):
        track = Mock()
        track.path = 'some_file.mp3'
        track.offset = 0
        with patch('subprocess.Popen') as popen_mock, \
                patch('threading.Thread') as thread_mock:
            mplayer_mock = Mock()
            mplayer_mock.stdout = []
            popen_mock.return_value = mplayer_mock
            self.sut.play_track(track)
            popen_mock.assert_called_once()
            mplayer_mock.stdin.write.assert_not_called()

    def test_seek_command_should_be_sent_if_tracks_are_same(self):
        mplayer_mock = Mock()
        mplayer_mock.stdout = []
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
            mplayer_mock.stdout = []
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
            mplayer_mock.stdout = []
            self.sut.play_track(track)
            popen_mock.assert_not_called()
            mplayer_mock.stdin.write.assert_called_once_with('seek 20 2 1\n')

    def test_backend_should_be_started_with_proper_ss_value_if_track_has_offset(self):
        mplayer_mock = Mock()
        mplayer_mock.stdout = []
        track = Mock()
        track.path = 'some_file.mp3'
        track.offset = 215
        with patch('subprocess.Popen') as popen_mock, \
                patch('threading.Thread') as thread_mock:
            # TODO: check popen args
            popen_mock.return_value = mplayer_mock
            self.sut.play_track(track)
            popen_mock.assert_called_once()

    def test_stop_should_be_ignored_if_no_track_playing(self):
        mplayer_mock = Mock()
        mplayer_mock.stdout = []
        self.sut.current_track = None
        self.sut.mplayer = mplayer_mock
        self.sut.stop()
        mplayer_mock.stdin.write.assert_not_called()

    def test_stop_should_send_command_if_track_playing(self):
        mplayer_mock = Mock()
        mplayer_mock.stdout = []
        self.sut.current_track = Mock()
        self.sut.mplayer = mplayer_mock
        self.sut.stop()
        mplayer_mock.stdin.write.assert_called_once_with('stop\n')

    def test_toggle_pause_should_be_ignored_if_no_track_playing(self):
        mplayer_mock = Mock()
        mplayer_mock.stdout = []
        self.sut.current_track = None
        self.sut.mplayer = mplayer_mock
        self.sut.toggle_pause()
        mplayer_mock.stdin.write.assert_not_called()

    def test_toggle_pause_should_send_command_if_track_playing(self):
        mplayer_mock = Mock()
        mplayer_mock.stdout = []
        self.sut.current_track = Mock()
        self.sut.mplayer = mplayer_mock
        self.sut.toggle_pause()
        mplayer_mock.stdin.write.assert_called_once_with('pause\n')

    def test_can_be_closed(self):
        self.sut.mplayer = None
        self.sut.quit()

    def test_can_be_closed_if_backend_running(self):
        mplayer_mock = Mock()
        mplayer_mock.stdout = []
        self.sut.mplayer = mplayer_mock
        self.sut.quit()
        mplayer_mock.stdin.write.assert_called_once_with('quit\n')

    def test_should_terminate_backend_if_it_doesnt_close(self):
        mplayer_mock = Mock()
        mplayer_mock.stdout = []
        mplayer_mock.wait.side_effect = RuntimeError('')
        self.sut.mplayer = mplayer_mock
        self.sut.quit()
        mplayer_mock.stdin.write.assert_called_once_with('quit\n')

    def test_can_seek(self):
        mplayer_mock = Mock()
        mplayer_mock.stdout = []
        self.sut.current_track = Mock()
        self.sut.mplayer = mplayer_mock
        self.sut.seek(20)
        mplayer_mock.stdin.write.assert_called_once_with('seek 20 2 1\n')

    def test_can_seek_percentage(self):
        mplayer_mock = Mock()
        mplayer_mock.stdout = []
        self.sut.current_track = Mock()
        self.sut.mplayer = mplayer_mock
        self.sut.seek_percentage(20)
        mplayer_mock.stdin.write.assert_called_once_with('seek 20 1\n')

    def test_can_seek_forward(self):
        mplayer_mock = Mock()
        mplayer_mock.stdout = []
        self.sut.current_track = Mock()
        self.sut.mplayer = mplayer_mock
        self.sut.seek_forward(20)
        mplayer_mock.stdin.write.assert_called_once_with('seek +20 0\n')

    def test_can_seek_backward(self):
        mplayer_mock = Mock()
        mplayer_mock.stdout = []
        self.sut.current_track = Mock()
        self.sut.mplayer = mplayer_mock
        self.sut.seek_backward(20)
        mplayer_mock.stdin.write.assert_called_once_with('seek -20 0\n')

    def test_seek_should_be_ignored_if_no_track_playing(self):
        mplayer_mock = Mock()
        mplayer_mock.stdout = []
        self.sut.current_track = None
        self.sut.mplayer = mplayer_mock
        self.sut.seek(20)
        self.sut.seek_percentage(20)
        self.sut.seek_forward(20)
        self.sut.seek_backward(20)
        mplayer_mock.stdin.write.assert_not_called()

    def test_can_set_volume(self):
        mplayer_mock = Mock()
        mplayer_mock.stdout = []
        self.sut.current_track = Mock()
        self.sut.mplayer = mplayer_mock
        self.sut.set_volume(20)
        mplayer_mock.stdin.write.assert_called_once_with('volume 20 1\n')

    def test_should_not_send_any_command_if_mplayer_is_not_running(self):
        mplayer_mock = Mock()
        mplayer_mock.stdout = []
        self.sut.current_track = Mock()
        self.sut.mplayer = None
        self.sut.set_volume(20)
        self.sut.seek(20)
        mplayer_mock.stdin.write.assert_not_called()

    def test_loadfile_and_seek_commands_should_be_sent_if_track_playing_and_paths_differ(self):
        last_track = Mock()
        last_track.path = 'file.flac'
        last_track.offset = 100
        mplayer_mock = Mock()
        self.sut.current_track = last_track
        self.sut.mplayer = mplayer_mock
        track = Mock()
        track.path = 'file2.mp3'
        track.offset = 20
        with patch('subprocess.Popen') as popen_mock, \
                patch('threading.Thread') as thread_mock:
            mplayer_mock.stdout = []
            self.sut.play_track(track)
            popen_mock.assert_not_called()
            mplayer_mock.stdin.write.has_calls(['loadfile \"file2.mp3\"\n', 'seek 20 2 1\n'])


class ArgumentsBuilderTests(TestCase):

    class Config(object):
        def __init__(self):
            pass


    def setUp(self):
        self.config_mock = self.Config()
        self.track_mock = Mock()
        self.track_mock.path = 'some_file.mp3'
        self.track_mock.offset = 0


    def assertHasPair(self, data, a, b):
        for i, e in enumerate(data):
            if e == a:
                if b:
                    self.assertEqual(data[i + 1], b)
                return
        raise RuntimeError('cannot find pair of {}, {}'.format(a, b))


    def assertHasItem(self, data, a):
        self.assertTrue(a in data)


    def assertDoesntHaveItem(self, data, a):
        self.assertFalse(a in data)


    def test_should_choose_default_values_if_no_config(self):
        self.config_mock.path = 'mplayer'
        sut = ArgumentsBuilder(self.config_mock)
        expected_args = ['mplayer', '-ao', 'pulse', '-noquiet', '-slave',
            '-novideo', '-cdrom-device', '/dev/sr0', '-vo', 'null', '-cache', '0', '-ss',
            '0', '-volume', '100', 'some_file.mp3']
        args = sut.build(self.track_mock)
        self.assertEqual(sorted(args), sorted(expected_args))


    def test_should_choose_proper_demuxer(self):
        self.config_mock.path = 'mplayer'
        self.config_mock.demuxer = {
            "mp3": "audio",
            "flac": "lavf",
            "ape": "ape"
        }
        sut = ArgumentsBuilder(self.config_mock)

        self.track_mock.path = 'some_file.mp3'
        args = sut.build(self.track_mock)
        self.assertHasPair(args, '-demuxer', 'audio')

        self.track_mock.path = 'some_file.flac'
        args = sut.build(self.track_mock)
        self.assertHasPair(args, '-demuxer', 'lavf')

        self.track_mock.path = 'some_file.eee'
        args = sut.build(self.track_mock)
        self.assertDoesntHaveItem(args, '-demuxer')

