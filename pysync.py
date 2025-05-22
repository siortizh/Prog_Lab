#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import threading
from collections import deque

class GenProdCons:
    def __init__(self, size=10):
        self.size = size
        self.buffer = deque()

    def __len__(self):
        return len(self.buffer)

    def put(self, val):
        self.buffer.append(val)
        return val

    def get(self):
        val = self.buffer.popleft()
        return val



class RendezvousDEchange:
    def __init__(self):
        self.lock = threading.Lock()
        self.thread_arrived = threading.Condition(self.lock)
        self.b_thread = False
        self.value = None

    def echanger(self, value):
        with self.lock:
            if not self.b_thread:
                self.value = value
                self.b_thread = True
                self.thread_arrived.wait()
                res = self.value
                self.b_thread = False
                self.thread_arrived.notify()
            else:
                res = self.value
                self.value = value
                self.thread_arrived.notify()
                self.thread_arrived.wait()
            return res