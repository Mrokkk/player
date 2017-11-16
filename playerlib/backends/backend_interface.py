#!/usr/bin/env python3

class Backend:

    def play_track(self, track):
        raise RuntimeError('Not implemented!')

    def toggle_pause(self):
        raise RuntimeError('Not implemented!')

    def stop(self):
        raise RuntimeError('Not implemented!')

    def seek(self, offset):
        raise RuntimeError('Not implemented!')

    def seek_percentage(self, percent):
        raise RuntimeError('Not implemented!')

    def seek_forward(self, time):
        raise RuntimeError('Not implemented!')

    def seek_backward(self, time):
        raise RuntimeError('Not implemented!')

    def set_volume(self, volume):
        raise RuntimeError('Not implemented!')

    def quit(self):
        raise RuntimeError('Not implemented!')

