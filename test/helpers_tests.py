#!/usr/bin/env python3

from unittest import TestCase
from unittest.mock import Mock
from urwim.helpers import *

class ClampTests(TestCase):
    def test_can_clamp_values(self):
        self.assertEqual(20, clamp(0, min_val=20))
        self.assertEqual(20, clamp(340, max_val=20))
        self.assertEqual(20, clamp(340, min_val=20, max_val=20))

