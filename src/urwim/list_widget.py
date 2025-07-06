#!/usr/bin/env python3

import urwid
from typing import Any, Callable

from .clipboard import *
from .helpers import *
from .widget import *

type Callback = Callable[[Any], None] | None

class ListWidget(urwid.ListBox, Widget):

    _readonly:  bool
    _on_delete: Callback
    _on_paste:  Callback

    def __init__(
        self,
        content: Any,
        readonly: bool = False,
        on_delete: Callback = None,
        on_paste: Callback = None
    ) -> None:
        self._readonly = readonly
        self._on_delete = on_delete
        self._on_paste = on_paste
        super().__init__(content)

    def _try_to_scroll(self, key: int) -> bool | None:
        try:
            if key == 5:
                if not self.body[self.focus_position + 1].selectable(): return
                self.focus_position += 1
                return True
            elif key == 4:
                if not self.body[self.focus_position - 1].selectable(): return
                self.focus_position -= 1
                return True
        except:
            pass

    def mouse_event(
        self,
        size: tuple[int, int],
        event,
        button: int,
        col: int,
        row: int,
        focus: bool,
    ) -> bool | None:
        if self._try_to_scroll(button):
            return None
        return super().mouse_event(size, event, button, col, row, focus)

    def keypress(
        self,
        size: tuple[int, int],
        key: str
    ) -> str | None:
        if key == 'home':
            # FIXME: check if element is selectable
            self.scroll_beginning()
            return None
        elif key == 'end':
            self.scroll_end()
            return None
        return super().keypress(size, key)

    def scroll_beginning(self) -> None:
        self.focus_position = 0

    def scroll_end(self) -> None:
        self.focus_position = len(self.body) - 1

    def search_forward(self, pattern: str) -> None:
        index = self.focus_position + 1
        while True:
            try:
                if pattern in self.body[index].text:
                    self.focus_position = index
                    return
                index += 1
            except:
                break

    def search_backward(self, pattern: str) -> None:
        index = self.focus_position - 1
        while True:
            try:
                if pattern in self.body[index].text:
                    self.focus_position = index
                    return
                index -= 1
                if index < 0: return
            except:
                break

    @property
    def readonly(self) -> bool:
        return self._readonly

    def _writeable_check(self) -> None:
        if self.readonly:
            raise RuntimeError('list is readonly')

    def delete(self) -> None:
        self._writeable_check()
        deleted = self.body[self.focus_position]
        del self.body[self.focus_position]
        if self._on_delete: self._on_delete(deleted)
        clipboard_set(deleted)

    def yank(self) -> None:
        if len(self.body) == 0: return
        yanked = self.body[self.focus_position]
        clipboard_set(yanked)

    def paste_after(self) -> None:
        self._writeable_check()
        entry = clipboard_get()
        self.body.insert(self.focus_position + 1 if self.focus_position else 0, entry)
        if self._on_paste: self._on_paste(entry)

    def paste_before(self) -> None:
        self._writeable_check()
        entry = clipboard_get()
        self.body.insert(self.focus_position - 1 if self.focus_position else 0, entry)
        if self._on_paste: self._on_paste(entry)

    @property
    def searchable_list(self):
        return self

