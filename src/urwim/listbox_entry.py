#!/usr/bin/env python3

import urwid

class ListBoxEntry(urwid.Button):

    def __init__(
        self,
        text: str,
        unfocused: str | None = None,
        focused: str | None = None
    ):
        super().__init__('')
        self.update(text, unfocused, focused)

    @property
    def text(self) -> str:
        '''Has to be implemented by subclass; used for searching in ListBox'''
        raise NotImplementedError('text property not implemented by widget')

    def update(
        self,
        text: str,
        unfocused: str | None = None,
        focused: str | None = None
    ) -> None:
        widget = urwid.SelectableIcon(text, 0)
        if unfocused and focused:
            widget = urwid.AttrMap(widget, unfocused, focused)
        self._w = widget

    def keypress(self, size: tuple[int], key: str) -> str | None:
        '''Ignore key presses'''
        return key

