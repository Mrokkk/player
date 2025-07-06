#!/usr/bin/env python3

import copy
from typing import Any

from .rdb import rdb

def clipboard_get() -> Any:
    return copy.deepcopy(rdb['clipboard'])

def clipboard_set(o: Any) -> Any:
    rdb['clipboard'] = copy.deepcopy(o)
