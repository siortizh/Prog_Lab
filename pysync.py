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
    
    def __init__(self):

        self.mutex = threading.Lock()

        self.rendezvous = threading.Condition(self.mutex)

        self.first_thread_arrived = False
        self.first_thread_value = None
        self.second_thread_value = None
    
    def echanger(self, value):

        with self.rendezvous:
            if not self.first_thread_arrived:

                self.first_thread_arrived = True
                self.first_thread_value = value

                self.rendezvous.wait()

                result = self.second_thread_value

                self.first_thread_arrived = False
                self.first_thread_value = None
                self.second_thread_value = None
                
                return result
            else:

                self.second_thread_value = value

                result = self.first_thread_value

                self.rendezvous.notify()
                
                return result