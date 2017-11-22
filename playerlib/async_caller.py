#!/usr/bin/env python3

import logging
import queue
import threading

class AsyncCaller:

    class Thread(threading.Thread):

        def __init__(self, queue):
            self.queue = queue
            super().__init__(daemon=True)

        def run(self):
            while True:
                async_job = self.queue.get()
                if async_job == None: break
                async_job()

    def __init__(self):
        self.queue = queue.Queue()
        self.thread = self.Thread(self.queue)
        self.thread.start()
        self.logger = logging.getLogger('AsyncCaller')

    def call(self, target):
        self.queue.put(target)

