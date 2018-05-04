#!/usr/bin/env python3

from unittest import TestCase
from unittest.mock import Mock
from playerlib.track.track import *

class TrackTests(TestCase):

    def test_can_be_converted_to_dict(self):
        track = Track()
        track.path = 'some_path'
        track.offset = 2
        track.length = 21
        track.index = 1
        track.title = 'title'
        track.artist = 'Artist'
        track.state = Track.State.PLAYING
        track.playlist_entry = Mock()
        dict_track = track.to_dict()
        self.assertEqual(dict_track['path'], 'some_path')
        self.assertEqual(dict_track['offset'], 2)
        self.assertEqual(dict_track['length'], 21)
        self.assertEqual(dict_track['index'], 1)
        self.assertEqual(dict_track['title'], 'title')
        self.assertEqual(dict_track['artist'], 'Artist')
        self.assertFalse('state' in dict_track)
        self.assertFalse('playlist_entry' in dict_track)

    def test_can_be_created_from_dict(self):
        dict_track = {
            'path': 'some_path',
            'offset': 23,
            'length': 315,
            'index': 98,
            'title': 'Some Title',
            'artist': 'Random Artist',
        }
        track = Track(dict_track)
        self.assertEqual(track.path, 'some_path')
        self.assertEqual(track.offset, 23)
        self.assertEqual(track.length, 315)
        self.assertEqual(track.index, 98)
        self.assertEqual(track.title, 'Some Title')
        self.assertEqual(track.artist, 'Random Artist')

    def test_play_sets_proper_state_and_triggers_playlist_entry(self):
        track = Track()
        track.playlist_entry = Mock()
        track.play()
        self.assertEqual(track.state, Track.State.PLAYING)
        track.playlist_entry.set_playing.assert_called_once()

    def test_toggle_pause_pauses_track_if_was_in_playing_state(self):
        track = Track()
        track.playlist_entry = Mock()
        track.state = Track.State.PLAYING
        track.toggle_pause()
        self.assertEqual(track.state, Track.State.PAUSED)
        track.playlist_entry.set_paused.assert_called_once()

    def test_toggle_pause_plays_track_if_was_in_paused_state(self):
        track = Track()
        track.playlist_entry = Mock()
        track.state = Track.State.PAUSED
        track.toggle_pause()
        self.assertEqual(track.state, Track.State.PLAYING)
        track.playlist_entry.set_playing.assert_called_once()

    def test_toggle_pause_does_nothing_if_was_in_stopped_state(self):
        track = Track()
        track.playlist_entry = Mock()
        track.state = Track.State.STOPPED
        track.toggle_pause()
        self.assertEqual(track.state, Track.State.STOPPED)
        track.playlist_entry.set_playing.assert_not_called()
        track.playlist_entry.set_stopped.assert_not_called()
        track.playlist_entry.set_paused.assert_not_called()

    def test_stop_sets_proper_state_and_triggers_playlist_entry(self):
        track = Track()
        track.playlist_entry = Mock()
        track.state = Track.State.PLAYING
        track.stop()
        self.assertEqual(track.state, Track.State.STOPPED)
        track.playlist_entry.set_playing.assert_not_called()
        track.playlist_entry.set_stopped.assert_called_once()
        track.playlist_entry.set_paused.assert_not_called()

