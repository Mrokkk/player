#!/usr/bin/env python3

from typing import Dict

class Track:

    class State:
        STOPPED = 0
        PLAYING = 1
        PAUSED = 2

    def __init__(self, dictionary=None) -> None:
        self.path = None
        self.offset = 0
        self.length = 0
        self.index = 0
        self.title = None
        self.artist = None
        self.album = None
        self.performer = None
        self.state = self.State.STOPPED
        self.playlist_entry = None
        if dictionary:
            self._from_dict(dictionary)

    def to_dict(self) -> Dict[str, str]:
        d = self.__dict__.copy()
        del d['state']
        del d['playlist_entry']
        return d

    def _from_dict(self, d: Dict[str, str]) -> None:
        for k, v in d.items():
            setattr(self, k, v)

    def play(self) -> None:
        self.state = self.State.PLAYING
        self.playlist_entry.set_playing()

    def _pause(self) -> None:
        self.state = self.State.PAUSED
        self.playlist_entry.set_paused()

    def toggle_pause(self) -> None:
        if self.state == self.State.PAUSED:
            self.play()
        elif self.state == self.State.PLAYING:
            self._pause()

    def stop(self) -> None:
        self.state = self.State.STOPPED
        self.playlist_entry.set_stopped()

    def __repr__(self) -> str:
        return str(self.to_dict())

