# -*- coding: utf-8 -*-
"""
Created on Wed Jan 16 18:41:30 2019

@author: USER
"""
import networkx as nx    
from networkx.algorithms import approximation
import sys
import random
from fractions import Fraction

class Sofda(object):
    def __init__(self, name, source, destination, Vms, SFC):
        """
         This method is used for initialization
        Args:
            G: networkx graph
            source: Source node in the network
            destination: destination node in the network
            Vms: List of nodes which where we can place Vms
            VNFS: number of Vnfs 

        """
#        
        #Parameters
        self.name = name
        self.source = source
        self.destination = destination
        self.Vms = Vms
        self.SFC = SFC
        
    def read_network(self):
        # Read the graphml ile
        """
        Reads the graphml file
        Returns:
        Graphml graph
        """
        g = nx.read_graphml(self.name)
        return g

    def k_Stroll(self, last_vm):
        # Function for generating k-Stroll of the network graph
        """
        Take VM, weight (which should be 'Cost', 'Delay' or 'Cost_Lemda') and 
        value of lemda (int) as arrguments
        Returns:
        K-stroll cost
        """

        G = self.read_network()
        for a in G.nodes():
            G.nodes[a]['Cost'] = 1
    
        #ac=nx.shortest_path(G, source='Los Angles', target='Dellas')
        c1 = {}
        source = self.source
        weight = 'Cost'
        cost_of_lastVM = G.nodes[str(last_vm)]['Cost']
        shortest_path_cost = {}
        for v1 in G.nodes():
    
            for v2 in G.nodes():
                c2 = 0
                cost = 0
                if v1 != v2:
                    c1 = nx. shortest_path(G, source=v1, target=v2, weight = 
                                           weight)
                    for a, b in zip(c1[0::1], c1[1::1]):
                        c2 = G. edges[a, b][weight]+c2
                        if source == G.nodes[v1]['id']:
                            cost = (cost_of_lastVM + G.nodes[v2]['Cost'])/2
                        elif source == G.nodes[v2]['id']:
                            cost = (cost_of_lastVM + G. nodes[v1]['Cost'])/2
                        else:
                            cost = (G.nodes[v1]['Cost'] +
                            G.nodes[v2]['Cost'])/2
                shortest_path_cost[(v1, v2)] = cost + c2
        return shortest_path_cost
    
    
    def Walk(self, last_vm):
    # Function for generating walk until last Vm
        """
        Take VM, weight (which should be 'Cost', 'Delay' or 'Cost_Lemda') and 
        value of lemda (int) as arrguments
        Returns:
        Path find by Walk
        """
        
        G = self.read_network()
        for a in G.nodes():
            G.nodes[a]['Cost'] = 1
        
        Cost_dash = self.k_Stroll(last_vm)
        destinations = self.destination
        source = self.source
        G_dash = G
        for x,y in G_dash.edges():
            G_dash.edges[x,y]['Cost'] = 1
        cost_node = {}
        weight = 'Cost'
        S = {}
        yv = {}
        source1 = str(source)
        Zs = 0
        InfessileWalk_flag=0
        for v in G.nodes():
            cost_node[v] = G.nodes[v]['Cost']
            if v == source1 or v in destinations:
                S[v] = 0
            elif G.nodes[v]['Cost'] > 0:
                S[v] = 1
            else:
                sys.exit('Cost is Negative and solution is not fesible')
        key_min = min(cost_node.keys(), key=(lambda k: cost_node[k]))
        Ebsilon = cost_node[key_min]
        cost_vert = 0
        c = {}
        walk_G = [source1]
        walk_t = []
        a = 0
        for s in G.nodes():
            if S[s] == 1 and s not in destinations:
                for src, des in G.edges():
                    if S[src] == 1 and S[des] == 0:
                        if Zs == G.edges[src, des][weight]:
                            c[a] = src, des
                            a += 1
                            if des == source1 or des in walk_G:
                                S[src] = 0
                                walk_G.append(src)
                    elif S[src] == 0 and S[des] == 1:
                        if Zs == G.edges[src, des][weight]:
                            c[a] = src, des
                            a += 1
                            if src == source1 or src in walk_G:
                                S[des] = 0
                                walk_G.append(des)
                    elif cost_node[key_min] == 0:
                        Ebsilon = 1
                    else:
                        Ebsilon = cost_node[key_min]
                ac = 0
                while S[s] == 1:
                    if cost_node[s] != 0:
                        ac += Ebsilon
                        cost_node[s] -= Ebsilon
                        yv[s] = ac
                        Zs += yv[s]
                    elif cost_node[s] == 0:
                        S[s] = 0
                        walk_t.append(s)
        u = str(last_vm)
        C = self.SFC
        merged_walk = walk_G + walk_t
        length = len(merged_walk)
        last_vm1 = merged_walk.index(u)+1
        del merged_walk[last_vm1 : length]
        
        length_mergedwalk = len(merged_walk)
        while length_mergedwalk != C+1:
            if length_mergedwalk < C+1:
                InfessileWalk_flag = 1
                break
            elif length_mergedwalk > C+1:
                length_mergedwalk = length_mergedwalk-1
                del merged_walk[-2]
            else:
                #do nothing
                print ""
        final_walk = []
        counter = 0
        cost = 0
        for a, b in zip(merged_walk[0::1], merged_walk[1::1]):
            if counter == 0:
                final_walk += nx.shortest_path(G, source=a, 
                                               target=b, weight= 'Cost')
                counter += 1
            else:
                ver = nx.shortest_path(G, source=a, target=b, weight= 'Cost')
                final_walk = final_walk+ver[1:len(ver)]
                counter += 1
        cost = self.cost_cal(final_walk)            
        
        return final_walk, InfessileWalk_flag, cost

    
    
    def cost_cal(self, walk):
    # Function for Calculating cost
        """
        Take path as arrguments which is obtained from walk
        Returns:
        Cost of the Path
        """
        Source_id = self.source
        final_walk = walk
        G = self.read_network()
        G_dash = G
        for a in G.nodes():
            G.nodes[a]['Cost'] = 1
    
        cost = 0
        flag = {}
        source = Source_id
        for a in final_walk:
            if int(a) == int(source):
                flag[a] = 0
            else: 
                flag[a] = 1
        ac = 0
    
        for a, b in zip(final_walk[0::1], final_walk[1::1]):
            if  flag[a] == 1 and flag[b] == 1:
    
                ac += G_dash.edges[a, b]['Cost']
                ac += G.nodes[b]['Cost']
                ac += G.nodes[a]['Cost']
                flag[b] = 0
                flag[a] = 0
                cost = ac
            elif flag[a] == 0 and flag[b] == 1:
                ac += G_dash.edges[a, b]['Cost']
                ac += G.nodes[b]['Cost']
                flag[b] = 0
                cost = ac
            else:
                ac += G.edges[a, b]['Cost']
                cost = ac
            
            
    
        return cost

        

topo = 'Ibm.graphml'
destination = ['15','16']
S = '17'
Vms = ['4','5','6']
last_vm = '5'

if __name__ == "__main__":
    newobject = Sofda(topo, S, destination, Vms, 3)
    a,b,c = newobject.Walk(last_vm)
    print a,c