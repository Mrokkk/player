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

