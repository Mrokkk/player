#!/usr/bin/env python3

import os
import sys
from unittest import TestCase
from unittest.mock import Mock, MagicMock, patch

from playerlib.command_panel import *

class TestCommandPanel(TestCase):

    def setUp(self):
        self.command_panel_mock = Mock()
        self.sut = CommandPanel(self.command_panel_mock)
        self.sut.set_edit_text = Mock()
        self.sut.set_caption = Mock()
        self.sut.set_edit_pos = Mock()

    def test_can_clear_view(self):
        self.sut.clear()
        self.sut.set_edit_text.assert_called_with('')
        self.sut.set_caption.assert_called_with('')

    def test_can_display_error(self):
        self.sut.error('Some error')
        self.sut.set_edit_text.assert_called_with('')
        self.sut.set_caption.assert_called_with(('error', 'Error: Some error'))

    def test_can_display_info(self):
        self.sut.info('Some info')
        self.sut.set_edit_text.assert_called_with('')
        self.sut.set_caption.assert_called_with(('info', 'Info: Some info'))

