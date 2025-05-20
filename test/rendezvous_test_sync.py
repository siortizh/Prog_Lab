# Test Basic

import os
import unittest
import importlib
from threading import Thread

expected_module = 'RENDEZVOUSMODULE'
default_module = 'pysyn'

if expected_module in os.environ:
    rendezvous_mdl = os.environ[expected_module]
else:
    rendezvous_mdl = 'pysync'

rendezvous_imprt = importlib.__import__(rendezvous_mdl, globals(), locals(), [], 0)

def thread(rdvs,val):
    return rdvs.echanger(val)

class TestProdConsTestSync(unittest.TestCase):

    
    def test_basic_concur(self):
        rendezvous = rendezvous_imprt.RendezvousDEchange()
        val_1 = 1
        val_2 = 2
        thread_1 = Thread(target=thread, args=(rendezvous, val_1))
        thread_2 = Thread(target=thread, args=(rendezvous, val_2))
        thread_1.run()
        thread_2.run()
        ret_thr_1 = thread_1.join()
        ret_thr_2 = thread_2.join()
        
        self.assertNotEqual(ret_thr_1, val_2)
        self.assertNotEqual(ret_thr_2, val_1)
