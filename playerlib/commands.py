#!/usr/bin/env python3

from playerlib.helpers.asynchronous import *
from playerlib.helpers.default_commands import *

class Commands(DefaultCommands):
    def __init__(self, context):
        self._context = context
        super().__init__()

    @asynchronous
    def add_to_playlist(self, path):
        self._context.playlist.add_to_playlist(path)

    @asynchronous
    def replace_playlist(self, path):
        self._context.playlist.add_to_playlist(path, clear=True)

    def clear_playlist(self):
        self._context.playlist.clear()

    @asynchronous
    def save_playlist(self, playlist_file):
        self._context.playlist.save_playlist(playlist_file)

    @asynchronous
    def load_playlist(self, playlist_file):
        self._context.playlist.load_playlist(playlist_file)

    def pause(self):
        self._context.playback_controller.pause()

    def stop(self):
        self._context.playback_controller.stop()

    def next(self):
        self._context.playback_controller.next()

    def prev(self):
        self._context.playback_controller.prev()

    def seek(self, value):
        self._context.playback_controller.seek(value)

    def add_bookmark(self, path):
        self._context.bookmarks.add(path)

    @asynchronous
    def change_dir(self, path):
        self._context.file_browser.change_dir(path)

    def set(self, key, value):
        if key == 'volume':
            self._context.playback_controller.set_volume(value)
        else:
            raise RuntimeError('No such key: {}'.format(key))

    def get(self, key):
        if key == 'volume':
            return self._context.playback_controller.get_volume()
        else:
            raise RuntimeError('No such key: {}'.format(key))

