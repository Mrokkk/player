#!/usr/bin/env python3

import urwim

import playerlib.context as ctx

class Commands(urwim.Commands):

    _context: ctx.Context

    def __init__(self, context: ctx.Context) -> None:
        self._context = context
        super().__init__()

    @urwim.asynchronous
    def add_to_playlist(self, path: str) -> None:
        self._context.playlist.add_to_playlist(path)

    @urwim.asynchronous
    def replace_playlist(self, path: str) -> None:
        self._context.playlist.add_to_playlist(path, clear_and_play=True)

    def clear_playlist(self) -> None:
        self._context.playlist.clear()

    @urwim.asynchronous
    def save_playlist(self, playlist_file: str) -> None:
        self._context.playlist.save_playlist(playlist_file)

    @urwim.asynchronous
    def load_playlist(self, playlist_file: str) -> None:
        self._context.playlist.load_playlist(playlist_file)

    def pause(self) -> None:
        self._context.playback_controller.pause()

    def stop(self) -> None:
        self._context.playback_controller.stop()

    def next(self) -> None:
        self._context.playback_controller.next()

    def prev(self) -> None:
        self._context.playback_controller.prev()

    def seek(self, value: str) -> None:
        self._context.playback_controller.seek(value)

    def add_bookmark(self, path: str = None) -> None:
        if path is None:
            path = self._context.file_browser.current_dir()
        self._context.bookmarks.add(path)

    @urwim.asynchronous
    def change_dir(self, path: str) -> None:
        self._context.file_browser.change_dir(path)

