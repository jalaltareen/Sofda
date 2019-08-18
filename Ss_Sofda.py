# -*- coding: utf-8 -*-
"""
Created on Tue May 15 19:08:42 2018

@author: USER
"""
# Real time implementation of SOFDA
import networkx as nx
from networkx.algorithms import approximation
import sys
import random
from fractions import Fraction






# Read network


def read_network(name):
# Read the graphml ile
    """
    Reads the graphml file
    Returns:
    Graphml graph
    """

    topo = name
    g = nx.read_graphml(topo)
    return g


def rand_demands():
    G = read_network(network)
    nodes = G.number_of_nodes() -1
    edges = G.number_of_edges()
    z = runs
    load_seed = 400 + z
    destination_seed = 200 + z
    source_seed = 100 + z
    vm_seed = 300 + z
    random.seed(load_seed)
    a=[]
    for c in range (0 , (edges)):
        a.append(random.choice([0, 1]))
    cost_edge = [x * 5 for x in a]

    destination_id = []
    random.seed(destination_seed)
    destination_id = random.sample(range(1, nodes), 5) 
    random.seed(source_seed)
    source_id = random.choice([i for i in range(1, nodes) if i not in
                               destination_id])
    random.seed(vm_seed)
    Vms = []
    for b in range(0,7):
        Vms.append(random.choice([i for i in range(1, nodes) if i not in
                               destination_id or source_id]))
    counter = 0
    cost = {}
    for a,c in G.edges():
        G.edges[a,c]['load'] = cost_edge[counter]
        counter += 1
        G.edges[a,c]['bandwidth'] = (45 -G.edges[a,
               c]['load'])
        cost[a,c] = Fraction(G.edges[a,c]['load'],
            G.edges[a,c]['bandwidth'])
        G.edges[a,c]['Cost'] = 1
    
    
    return destination_id, source_id, Vms, G
# Read Set of Destinations


def read_demand(name):
# function for reading demand file
    """
    Reads the demand .txt file
    Returns:
    Destination_id, Source_id
    """    
    filename = name + '.txt'
    fp = open(filename, 'rt')
    lines='a'
    line=fp.readlines()
    fp.close()
    List = line[0]
    List2 = line[1]
    list3 = line[2]
    a=List.split(':')


    if a[0] == 'Destination':
        destination = a[1:]
    
    if '/n' in a:
        a = a.remove('/n')

    b = List2.split(',')
        
    if '/n' in b:
        b = b.remove('/n')
        
    if b[0] == 'Source':
        Source = b[1:]
    
    Vm_list = list3.split(':')
    if Vm_list[0] == 'Vm':
        Vm = Vm_list[1:]
    
#    if '/n' in a:
#        a = a.remove('/n')
#        
#    if '/n' in Vm_list:
#        Vm_list = Vm_list.remove('/n')
#        

    G = read_network(network)
    Dic = {}
    Destinations=[]
    c=0
    Vm_id = []

    for g in G.nodes():
        Dic[g] = G.nodes[g]['label']
        if Source[0] == G.nodes[g]['label']:
            Source_id = G.nodes[g]['id']
        for vm in Vm:
            if vm ==  G.nodes[g]['label']:
                Vm_id.append(str(G.nodes[g]['id']))
            
        for a in destination:
            if a == G.nodes[g]['label']:
                Destinations.append(str(G.nodes[g]['id']))                

    return Destinations, Source_id
# Test input data


def k_Stroll(last_vm, Cost_or_delay, lemda):
# Function for generating k-Stroll of the network graph
    """
    Take VM, weight (which should be 'Cost', 'Delay' or 'Cost_Lemda') and 
    value of lemda (int) as arrguments
    Returns:
    K-stroll cost
    """

    G = read_network(network)
    for a in G.nodes():
        G.nodes[a]['Cost'] = 1

    #ac=nx.shortest_path(G, source='Los Angles', target='Dellas')
    c1 = {}
    destinations, source, vms, G_dash = rand_demands()
    weight = Cost_or_delay
    if weight == 'Cost_Lemda':
        for a,b in G_dash.edges():
            G_dash.edges[a,b]['Cost_Lemda'] = G_dash.edges[a,b][
                    'Cost'] + G_dash.edges[a,b]['Delay']* lemda 
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


def Walk(last_vm, Cost_or_delay, lemda):
# Function for generating walk until last Vm
    """
    Take VM, weight (which should be 'Cost', 'Delay' or 'Cost_Lemda') and 
    value of lemda (int) as arrguments
    Returns:
    Path find by Walk
    """
    
    G = read_network(network)
    for a in G.nodes():
        G.nodes[a]['Cost'] = 1
    
    Lemda = lemda
    Cost_dash = k_Stroll(last_vm, Cost_or_delay,Lemda )
    destinations, source, vms, G_dash = rand_demands()
    cost_node = {}
    weight = Cost_or_delay
    if weight == 'Cost_Lemda':
        for a,b in G_dash.edges():
            G_dash.edges[a,b]['Cost_Lemda'] = G_dash.edges[a,b][
                    'Cost'] + G_dash.edges[a,b]['Delay']* lemda 
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
    C = 3

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
    cost = cost_cal(final_walk)            

    return final_walk, InfessileWalk_flag

def cost_cal(walk):
# Function for Calculating cost
    """
    Take path as arrguments which is obtained from walk
    Returns:
    Cost of the Path
    """
    Destinations, Source_id, u, G_dash =rand_demands()
    final_walk = walk
    G = read_network(network)
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


def stiner_Cost(Stiner_edge):
# Function for Calculating cost of Stiner-Tree from last Vm till destinations
    """
    Take path from Stiner_graph as arrguments
    Returns:
    Cost of the Path
    """
    Destinations, Source_id, u, G_dash =rand_demands()
    ac = Stiner_edge
    xy = 0
    G = read_network(network)
    for a in G.nodes():
        G.nodes[a]['Cost'] = 1

    for c, b in zip(ac[0::2], ac[1::2]):
        xy += G_dash.edges[c, b]['Cost']

    return xy
    

def delay_cal(path):
# Function for Calculating delay
    """
    Take path as arrguments which is obtained from walk
    Returns:
    Delay of the Path
    """
    final_walk = path
    G = read_network(network)
    delay = 0
    flag = {}
    Destination_id, source = read_demand(demand)
    
    for a in final_walk:
        if int(a) == int(source):
            flag[a] = 0
        else: 
            flag[a] = 1
    ac = 0

    for a, b in zip(final_walk[0::1], final_walk[1::1]):
        if  flag[a] == 1 and flag[b] == 1:

            ac += G.edges[a, b]['Delay']
            ac += G.nodes[b]['Cost']
            ac += G.nodes[a]['Cost']
            flag[b] = 0
            flag[a] = 0
            delay = ac
        elif flag[a] == 0 and flag[b] == 1:
            ac += G.edges[a, b]['Delay']
            ac += G.nodes[b]['Cost']
            flag[b] = 0
            delay = ac
        else:
            ac += G.edges[a, b]['Delay']
            delay = ac

    return delay


def stiner_Delay(Stiner_graph):
# Function for Calculating delay of Stiner-Tree from last Vm till destinations
    """
    Take path from Stiner_graph as arrguments
    Returns:
    Delay of the Path
    """

    ac = Stiner_graph
    delay_stiner = 0
    G = read_network(network)
    for c, b in zip(ac[0::2], ac[1::2]):
        delay_stiner += G.edges[c, b]['Delay']
    return delay_stiner



def Single_Source(netwrok, location, Weight, lemda):
#Function for SS_Sofda 
    """
    Take network,demands weight (which should be 'Cost', 'Delay' or
    'Cost_Lemda') and value of lemda (int) as arrguments
    Returns:
    Final forest and Cost of it
    """

    G = read_network(netwrok)
    for a in G.nodes():
        G.nodes[a]['Cost'] = 1

    C = float('Inf')
    weight = Weight
    Destinations, Source_id, u, G_dash =rand_demands()
    list_1 = []
    Final_walk = []
    destination = Destinations[1]
    D_in_string = []
    for a in Destinations:
        D_in_string.append(str(a))
    Lemda = lemda
    for vm in u:
        ax = []
        ax.append(str(vm))
        cost_stiner = 0
        cost_temp = float('inf')
        Walk1, InfessileWalk_flag1 = Walk(vm, weight, Lemda)
        terminal_nodes = ax + D_in_string
        Walk_Cost = cost_cal(Walk1)
        if InfessileWalk_flag1 == 0:
            F_temp = approximation.steiner_tree(G,terminal_nodes, 'Cost')
            stiner_path = {}

            for a,b in F_temp.edges():
                if a in Destinations:
                    list_1 = []
                    list_1.append(a)
                    list_1.append(b)
                    stiner_path[a] = list_1
                    destination = a
                else:
                    list_1.append(a)
                    list_1.append(b)
                    stiner_path[destination] = list_1
            list_1=[]
            stiner = []
            for a in stiner_path:
                stiner += stiner_path[a]

            cost_stiner = stiner_Cost(stiner)
            cost_temp = cost_stiner + Walk_Cost
            if cost_temp < C:
                stiner1 = stiner
                C = cost_temp
                F = F_temp.edges()
                Final_Walk = Walk1
                last_vm = vm
        else:
            pass
    print list(set(stiner)), last_vm, Final_Walk
    return C

#Public Variables
network ='Ibm.graphml'
demand = 'destination_set'

for runs in range (1,2):
    Single_Source(network, demand, 'Cost', 0) #line to test the inputs
