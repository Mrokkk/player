#!/usr/bin/env python3

class Rdb(dict):

    def __init__(self):
        super().__init__()
        self._subscriptions = {}

    def __getitem__(self, key):
        return super().__getitem__(key)

    def __setitem__(self, key, value):
        try:
            old_value = self[key]
        except: old_value = None
        super().__setitem__(key, value)
        if key in self._subscriptions:
            for sub in self._subscriptions[key]:
                sub(old_value, value)

    def subscribe(self, key, callback):
        if key not in self:
            super().__setitem__(key, None)
        if key not in self._subscriptions:
            self._subscriptions[key] = []
        self._subscriptions[key].append(callback)

    def unsubscribe(self, key):
        # TODO
        pass

