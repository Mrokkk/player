#!/usr/bin/env python3

import urwim

class Bookmark(urwim.ListBoxEntry):

    _index: int
    _path:  str

    def __init__(self, index: int, path: str) -> None:
        self._index = index
        self._path = path
        super().__init__([str(index), ' ', self._path], 'file', 'file_focused')

    @property
    def text(self) -> str:
        return self._path

    @property
    def index(self) -> int:
        return self._index

    @index.setter
    def index(self, index: int) -> None:
        self._index = index
        self.update([str(index), ' ', self._path], 'file', 'file_focused')

    def __repr__(self) -> str:
        return str(self.__dict__)

