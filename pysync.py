#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import threading
from collections import deque

class GenProdCons:
    
    def __init__(self, size=10):

        if size <= 0:
            raise ValueError("El tamaño del buffer debe ser mayor que 0")
        
        self.size = size
        self.buffer = deque(maxlen=size)

        self.mutex = threading.Lock()

        self.empty_slots = threading.Semaphore(size)
        self.filled_slots = threading.Semaphore(0)
    
    def __len__(self):

        with self.mutex:
            return len(self.buffer)
    
    def put(self, item):

        self.empty_slots.acquire()

        with self.mutex:
            self.buffer.append(item)

        self.filled_slots.release()
    
    def get(self):

        self.filled_slots.acquire()

        with self.mutex:
            item = self.buffer.popleft()

        self.empty_slots.release()
        
        return item


class RendezvousDEchange:
    def _init_(self):
        self.lock = threading.Lock()
        self.value = None
        self.partner_ready = threading.Condition(self.lock)
        self.has_partner = False

    def echanger(self, value):
        with self.lock:
            if not self.has_partner:
                # First thread arrives
                self.value = value
                self.has_partner = True
                self.partner_ready.wait()
                result = self.value
                self.has_partner = False
                self.partner_ready.notify()
                return result
            else:
                # Second thread arrives
                result = self.value
                self.value = value
                self.partner_ready.notify()
                self.partner_ready.wait()
                
                return result