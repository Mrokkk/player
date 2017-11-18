#!/usr/bin/env python3

from unittest import TestCase
from unittest.mock import Mock, MagicMock, patch
from playerlib.helpers.scrollable import *

class ScrollableTests(TestCase):

    def setUp(self):
        self.listbox = Mock()

    def test_can_scroll_listbox_down(self):
        self.listbox.focus_position = 10
        try_to_scroll(self.listbox, ('mouse press', 5.0))
        self.assertEqual(self.listbox.focus_position, 11)
        try_to_scroll(self.listbox, ('mouse press', 5.0))
        self.assertEqual(self.listbox.focus_position, 12)

    def test_can_scroll_listbox_up(self):
        self.listbox.focus_position = 10
        try_to_scroll(self.listbox, ('mouse press', 4.0))
        self.assertEqual(self.listbox.focus_position, 9)
        try_to_scroll(self.listbox, ('mouse press', 4.0))
        self.assertEqual(self.listbox.focus_position, 8)

    def test_ignores_exceptions(self):
        self.listbox.focus_position.side_effect = KeyError
        try_to_scroll(self.listbox, ('mouse press', 4.0))

    def test_ignores_other_keypresses(self):
        self.listbox.focus_position = 10
        try_to_scroll(self.listbox, ('mouse press', 6.0))
        self.assertEqual(self.listbox.focus_position, 10)
        self.listbox.focus_position = 10
        try_to_scroll(self.listbox, 'a')
        self.listbox.focus_position = 10

