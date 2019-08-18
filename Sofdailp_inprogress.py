from gurobipy import GRB, Model
import networkx as nx    

class SofdaiLp(object):
    def __init__(self, G, source, destination, Vms, VNFS):
        """
         This method is used for initialization
        Args:
            G: networkx graph
            source: Source node in the network
            destination: destination node in the network
            Vms: List of nodes which where we can place Vms
            VNFS: number of Vnfs 

        """
        self.model = Model()
#        self.enabled_vm = dict()
#        self.edge = dict()
        self.Vars = dict()
        self.F = list()

#        
        #Parameters
        self.G = G
        self.source = source
        self.destination = destination
        self.Vms = Vms
        self.VNFS = VNFS
        
        
    
    def check_source(self):
        """
        It check that source is the part of the network or invalid source. if 
        invalid then raise exception
        Return:
            True or false
        """
        source_bool = False
        for a in G.nodes():
            if a in self.source:
                source_bool = True
        if source_bool == False:
            raise Exception('Source is not in Network')
            
        return source_bool
    
    def check_destination(self):
        """
        It check that destination is the part of the  network or invalid 
        destination. if invalid then raise exception
        Return:
            True or false
        """
        destination_bool = {}
        destinations_bool = False
        for b in self.destination:
            destination_bool[b] = False
        for a in G.nodes():
            if a in self.destination:
                destination_bool [a] = True
                
        for c in destination_bool:
            if destination_bool[c] == False:
                raise Exception('Destination is not in Network')
            else:
                destinations_bool = True
            
            
        return destinations_bool


    def check_Vms(self):
        """
        It check that Vms is the part of the  network. if invalid then raise 
        exception.
        Return:
            True or false
        """
        vm_bool = {}
        vms_bool = False
        for b in self.Vms:
            vm_bool[b] = False
        for a in G.nodes():
            if a in self.Vms:
                vm_bool [a] = True
                

        for c in vm_bool:
            if vm_bool[c] == False:
                raise Exception('Node for Vm assignment is not in Network')
            if c in self.source:
                raise Exception('Source is assgined as VM')
            if c in self.destination:
                raise Exception('Destination is assnied as VM')
            else:
                vms_bool = True
            
        return vms_bool
    
    
    def Creatvarriables(self):  # for creating decision varriables q,x,y,p
        """
        This method creates Gurobi Decision Varriables
        r_: denote if node u is assigned as the enabled VM for VNF f in the 
            walk to destination d.
        lemda : denote if edge e u,v is located in the walk connecting the 
                enabled VM of VNF f and the enabled VM of the next VNF fN.
        lemda2 : denote if edge e v,u is located in the walk connecting the 
                enabled VM of VNF f and the enabled VM of the next VNF fN.
        T_:     if edge e u,v is located in the forest.
        o_:     represents if node u is assigned as the enabled VM of service f
                for the whole service forest.
        """
        self.F = self.source + self.VNFS
        
        self.r_template = "r_{:s}_{:s}_{:s}"
        self.lembda_template = "lambda_{:s}_{:s}_{:s}_{:s}"
        self.T_template = "T_{:s}_{:s}_{:s}"
        self.o_template = "o_{:s}_{:s}"
        self.lambda2_template = "lambda2_{:s}_{:s}_{:s}_{:s}"
        self.r1_template = "r_{:s}_{:s}_{:s}"
        
        for d in self.destination:
            for f in G.nodes():
                for u in G.nodes():
                    name = self.r_template.format(d, f, u)
                    self.Vars[name] = self.model.addVar(
                                lb=0, vtype=GRB.BINARY, name = name)
    
                for u,v in G.edges():
                        name_lembda = self.lembda_template.format(d, f, u, v)
                        self.Vars[name_lembda] = self.model.addVar(
                                lb=0, vtype=GRB.BINARY, name= name_lembda)
                for u,v in G.edges():
                        name_T = self.T_template.format(f, u, v)
                        self.Vars[name_T] = self.model.addVar(
                                lb=0, vtype=GRB.BINARY, name= name_T)
                for u in G.nodes():
                        name_o = self.o_template.format(f, u)                    
                        self.Vars[name_o] = self.model.addVar(
                                lb=0, vtype=GRB.BINARY, name= name_o)
                for u,v in G.edges():
                        name_lambda2 = self.lambda2_template.format(d, f, v, u)
                        self.Vars[name_lambda2] = self.model.addVar(
                                lb=0, vtype=GRB.BINARY, name= name_lambda2)
                
        for d in self.destination:
            for fn in self.VNFS:
                for u in G.nodes():
                    name_r1 = self.r1_template.format(d, f, u)
                    self.Vars[name_r1] = self.model.addVar(
                                lb=0, vtype=GRB.BINARY, name= name_r1)

        self.model.update()

    def Source_Selection(self):

        """
        Constraint 1 ensures that each destination chooses one source s in S
        as its service source.
        Returns:
            None
        """
        self.add_fs = 0
        for d in self.destination:
            for f in self.source:
                for s in self.source:
                    name_r =self.r_template.format(d, f, s)
                    add1 = self.model.getVarByName(name_r)
                    
                    self.add_fs = self.add_fs + add1
        self.model.addConstr(self.add_fs, GRB.EQUAL, 1)
    
    
    def enabled_VM(self):
        
        """
        Constraint 2 finds a node u from M as the enaled VM of each VNF f for
        each destination.
        Returns:
            None
        """
        self.add = 0
        for d in self.destination:
            for f in self.source:
                for u in self.Vms:
                    name_r =self.r_template.format(d, f, u)
                    add1 = self.model.getVarByName(name_r)
                    
                    self.add = self.add + add1
        self.model.addConstr(self.add, GRB.EQUAL, 1)
        

    def destination_assignment1(self):
        
        """
        There are two constraints which deals with assignment of destinations
        for Function Fd. Constraint 3 is the 1st one in that
        Constraint 3 assign only one destination for Function Fd
        Returns:
            None
        """
        self.assign = 0
        for d in self.destination:
            for f in self.destination:
                for u in self.destination:
                    name_r =self.r_template.format(d, f, u)
                    self.assign = self.model.getVarByName(name_r)
                        
                self.model.addConstr(self.assign, GRB.EQUAL, 1)


    def destination_assignment2(self):
        
        """
        The 2nd constraint for destination assignment
        Contraint 4 assign only one destination for Function Fd
        Returns:
            None
        """
        self.add1 = 0
        for d in self.destination:
            for f in self.source:
                for u in self.Vms:
                    name_r =self.r_template.format(d, f, u)
                    add2 = self.model.getVarByName(name_r)
                        
                    self.add1 = add2
                self.model.addConstr(self.add1, GRB.EQUAL, 0)


    def assignment_of_enabled_VM(self):
        
        """
        Contraint 5 assign u as the enabled VM of VNF f for the whole service
        forest if u has been selected by atleast one destination d for VNF f
        Returns:
            None
        """
        for d in self.destination:
            for f in self.VNFS:
                for u in G.nodes():
                    name_r = self.r_template.format(d, f, u)
                    name_o = self.o_template.format(f, u)
                    LHS = self.model.getVarByName(name_r)
                    RHS = self.model.getVarByName(name_o)
        self.model.addConstr(LHS, GRB.LESS_EQUAL, RHS)
 
    
    def atmost_one_VNF(self):
        
        """
        Contraint 6 ensures that each node u is in charge of at most one VNF.
        Returns:
            None
        """
        self.sum_o = 0
        for f in self.VNFS:
            for u in G.nodes():
                name_o = self.o_template.format(f, u)
                RHS = self.model.getVarByName(name_o)
                self.sum_o += RHS
        self.model.addConstr(self.sum_o, GRB.LESS_EQUAL, 1)

        
    def routing_of_service_chain(self):
        """
        Contraint 7 It first finds the routing of the service chain for each 
        destination d. It ensures that at least one edge eu;v incident from u
        is selected for the service chain because no edge e v;u incident 
        to u is chosen
        Returns:
            None
        """
        add_lemda1 = 0
        add_lemda2 = 0
        self.final_lemda = 0
        for d in self.destination:
            for f in self.F:
                for u,v in G.edges():
                    name_lembda = self.lembda_template.format(d, f, u, v)
                    LS = self.model.getVarByName(name_lembda)
                    add_lemda1 += LS
        for d in self.destination:
            for f in self.F:
                for u,v in G.edges():
                    name_lembda2 = self.lambda2_template.format(d, f, v, u)
                    RS = self.model.getVarByName(name_lembda2)
                    add_lemda2 += RS
                    
        self.final_lemda = add_lemda1 - add_lemda2
        
        for d in self.destination:
            for f in self.F:
                for fn in self.VNFS:
                    for u in G.nodes():
                        name_r = self.r_template.format(d, f, u)
                        name_r1 = self.r1_template.format(d, fn, u)
                        LS1 = self.model.getVarByName(name_r)
                        RS1 = self.model.getVarByName(name_r1)
                        final_r = LS1 - RS1
                        
                        self.model.addConstr(self.final_lemda, 
                                             GRB.GREATER_EQUAL, final_r)
                        
                        
    def edge_inthe_service_forest(self):
        """
        Contraint 8 states that any edge e u;v is in the service forest if it
        is in the service chain for at least one destination d..
        Returns:
            None
        """
        for d in self.destination:
            for f in self.F:
                for u,v in G.edges():
                    name_lembda = self.lembda_template.format(d, f, u, v)
                    name_T = self.T_template.format(f, u, v)
                    LS = self.model.getVarByName(name_lembda)
                    RS = self.model.getVarByName(name_T)
                    self.model.addConstr(LS, GRB.LESS_EQUAL, RS)

                    
    def optimzation(self):
        cost_nodes = 0
        cost_edges = 0
        for f in self.VNFS:
            for u in G.nodes:
                name_o =self.o_template.format(f, u)
                LS = G.nodes[u]['Cost'] * self.model.getVarByName(name_o)
                cost_nodes += LS 
        for f in self.VNFS:
            for u,v in G.edges():
                name_T = self.T_template.format(f, u, v)
                RS = G.edges[u,v]['Cost'] * self.model.getVarByName(name_T)
                cost_edges += RS
        final_cost = cost_nodes + cost_edges
        self.model.setObjective(final_cost, GRB.MINIMIZE)
        self.model.optimize()
        status = self.model.status

        return status
    
    def build(self):
            self.check_source()
            self.check_destination()
            self.check_Vms()
            self.Creatvarriables()
            self.Source_Selection()
            self.enabled_VM()
            self.destination_assignment1()
            self.destination_assignment2()
            self.assignment_of_enabled_VM()
            self.atmost_one_VNF()
            self.routing_of_service_chain()
            self.edge_inthe_service_forest()
    
    
        

topo = 'Ibm.graphml'
G = nx.read_graphml(topo)
destination = ['15','16']
vnfs = ['1','2','3','4','5']
S = ['1']
Vms = ['4','5','6','7','8']

for u in G.nodes():
    G.nodes[u]['Cost'] = 1
for u,v in G.edges():
    G.edges[u,v]['Cost'] = 1
 
        
if __name__ == "__main__":
    newobject = SofdaiLp(G, S, destination, Vms, vnfs)
    newobject.build()
    newobject.optimzation()

