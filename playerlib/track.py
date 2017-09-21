#!/usr/bin/env python3

class Track:

    class State:
        STOPPED = 0
        PLAYING = 1
        PAUSED = 2

    def __init__(self, file_path):
        self.path = file_path
        self.offset = 0 # For CUE sheets
        self.length = 0
        self.index = 0
        self.title = None
        self.artist = None
        self.performer = None
        self.state = self.State.STOPPED
        self.playlist_entry = None

    def play(self):
        self.state = self.State.PLAYING
        self.playlist_entry.select()

    def toggle_pause(self):
        if self.state == self.State.PAUSED:
            self.state = self.State.PLAYING
            self.playlist_entry.select()
        elif self.state == self.State.PLAYING:
            self.state = self.State.PAUSED
            self.playlist_entry.pause()

    def stop(self):
        self.state = self.State.STOPPED
        self.playlist_entry.unselect()

