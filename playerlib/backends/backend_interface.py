#!/usr/bin/env python3

class Backend:

    def play_track(self, track):
        raise NotImplementedError('Not implemented!')

    def toggle_pause(self):
        raise NotImplementedError('Not implemented!')

    def stop(self):
        raise NotImplementedError('Not implemented!')

    def seek(self, offset):
        raise NotImplementedError('Not implemented!')

    def seek_percentage(self, percent):
        raise NotImplementedError('Not implemented!')

    def seek_forward(self, time):
        raise NotImplementedError('Not implemented!')

    def seek_backward(self, time):
        raise NotImplementedError('Not implemented!')

    def set_volume(self, volume):
        raise NotImplementedError('Not implemented!')

    def quit(self):
        raise NotImplementedError('Not implemented!')

