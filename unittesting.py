# -*- coding: utf-8 -*-
"""
Created on Sat Aug 04 20:40:27 2018

@author: USER
"""

import unittest

import Sofdailp_inprogress
import networkx as nx



class TestCalc(unittest.TestCase):

    def setUp(self):
        self.a = Sofdailp_inprogress.SofdaiLp(G, S, destination, Vms, vnf)
        self.b = Sofdailp_inprogress.SofdaiLp(G, S1, destination, Vms, vnf)
    
    def test_source(self):
        s = len(S)
        self.assertEqual(self.a.check_source(), True)
        self.assertGreater(s, 0)
        
        
    def test_dest(self):
        d = len(destination)
        self.assertEqual(self.a.check_destination(), True)
        self.assertGreater(d, 0)
        

    def test_vms(self):
        v = len(Vms)
        self.assertEqual(self.a.check_Vms(), True)
        self.assertGreater(v, 0)
    
    
    def test_model(self):
        self.a.build()
        self.assertEqual(self.a.optimzation(), 2)
        self.assertEqual(self.b.optimzation(), 2)

topo = 'Ibm.graphml'
G = nx.read_graphml(topo)
destination = ['15','16']
vnf = [1,2,3,4,5]
S1 = [1]
Vms = ['4','5','6','7','8']
S = ['1']
for u in G.nodes():
    G.nodes[u]['Cost'] = 1
for u,v in G.edges():
    G.edges[u,v]['Cost'] = 1
    
F = S + vnf
        

if __name__ == '__main__':
    unittest.main()
