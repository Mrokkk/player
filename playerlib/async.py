#!/usr/bin/env python3

import functools
import logging
import queue
import threading
from playerlib.helpers.helpers import *

def async(f):
    '''Decorator which allows any function to be called asynchronously'''

    class AsyncCaller:
        class __caller:
            class Thread(threading.Thread):
                def __init__(self, queue, logger):
                    self.queue = queue
                    self.logger = logger
                    super().__init__(daemon=True)

                def run(self):
                    while True:
                        async_job = self.queue.get()
                        if async_job == None: break
                        try:
                            async_job()
                        except:
                            log_exception(self.logger)

            def __init__(self):
                self.logger = logging.getLogger('AsyncCaller')
                self.queue = queue.Queue()
                self.thread = self.Thread(self.queue, self.logger)
                self.thread.start()

            def call(self, target):
                self.queue.put(target)

        _instance = None

        def __new__(a):
            if AsyncCaller._instance is None:
                AsyncCaller._instance = AsyncCaller.__caller()
            return AsyncCaller._instance


    @functools.wraps(f)
    def _async_call(*args, **kwargs):
        AsyncCaller().call(lambda: f(*args, **kwargs))
    return _async_call

