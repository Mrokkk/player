#!/usr/bin/env python3

import urwim

class Commands(urwim.Commands):
    def __init__(self, context):
        self._context = context
        super().__init__()

    @urwim.asynchronous
    def add_to_playlist(self, path):
        self._context.playlist.add_to_playlist(path)

    @urwim.asynchronous
    def replace_playlist(self, path):
        self._context.playlist.add_to_playlist(path, clear_and_play=True)

    def clear_playlist(self):
        self._context.playlist.clear()

    @urwim.asynchronous
    def save_playlist(self, playlist_file):
        self._context.playlist.save_playlist(playlist_file)

    @urwim.asynchronous
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

    def add_bookmark(self, path=None):
        if path is None:
            path = self._context.file_browser.current_dir()
        self._context.bookmarks.add(path)

    @urwim.asynchronous
    def change_dir(self, path):
        self._context.file_browser.change_dir(path)

