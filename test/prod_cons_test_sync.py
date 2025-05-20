# Test Basic

import os
import unittest
from threading import Thread
import importlib

expected_module = 'PRODCONSMODULE'
default_module = 'pysyn'

if expected_module in os.environ:
    prod_cons_mdl = os.environ[expected_module]
else:
    prod_cons_mdl = 'pysync'

prod_cons_imprt = importlib.__import__(prod_cons_mdl, globals(), locals(), [], 0)

def basic_producer(prod_cons,times=100):
    prod_values = []
    for i in range(0,times):
        prod_cons.put(i)
        prod_values.append(i)

    return prod_values

def basic_consumer(prod_cons,times=100):
    cons_values = []
    for i in range(0,times):
        cons_values.append(prod_cons.get())
        
    return cons_values

class TestProdConsTestSync(unittest.TestCase):

    
    def test_prod_cons_all(self):
        prod_cons = prod_cons_imprt.GenProdCons()
        prod_thr = Thread(target=basic_producer,args=(prod_cons,100))
        cons_thr = Thread(target=basic_consumer,args=(prod_cons,100))
        prod_thr.start()
        cons_thr.start()
        prod_values = prod_thr.join()
        cons_values = cons_thr.join()
        self.assertEqual(prod_values,cons_values)
