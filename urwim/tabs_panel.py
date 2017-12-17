#!/usr/bin/env python3

import urwid

class TabsPanel(urwid.WidgetWrap):

    def __init__(self, tabs):
        self._tabs = tabs
        super().__init__(urwid.Columns([], dividechars=1))
        for i, t in enumerate(tabs):
            self.add_tab(t, selected=i==0)

    def _selected_tab(self, index, name):
        return (
            urwid.AttrMap(urwid.SelectableIcon(' ' + str(index + 1) + ' ' +  name + ' '), 'tab_active'),
            self._w.options('pack')
        )

    def _unselected_tab(self, index, name):
        return (
            urwid.AttrMap(urwid.SelectableIcon(' ' + str(index + 1) + ' ' +  name + ' '), 'tab_inactive'),
            self._w.options('pack')
        )

    def add_tab(self, tab, selected=False):
        if selected:
            self._w.contents.append(self._selected_tab(len(self._w.contents), tab.name))
        else:
            self._w.contents.append(self._unselected_tab(len(self._w.contents), tab.name))

    def select(self, index):
        for i, t in enumerate(self._tabs):
            if index == i:
                self._w.contents[i] = self._selected_tab(i, t.name)
            else:
                self._w.contents[i] = self._unselected_tab(i, t.name)

    def update(self, index):
        self._w.contents[index] = self._selected_tab(index, self._tabs[index].name)

    def selectable(self):
        return False

