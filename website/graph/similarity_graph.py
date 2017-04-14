from .graph import Graph
from .graph import Edge
from ..tree.tree import Tree

class SimilarityGraph(Graph):
    def __init__(self, T1, T2):
        super().__init__()
        self.T1 = T1
        self.T2 = T2

    def get_error(self, T1, T2):
        if(str(T1.element) == str(T2.element)):
            return 0
        return 1

    def create_graph(self):
        T1_list = self.T1.create_node_list()
        T2_list = self.T2.create_node_list()

        for i in range(1, len(T1_list)):
            for j in range(1, len(T2_list)):
                if(T1_list[i].depth == T2_list[j].depth):
                    error = self.get_error(T1_list[i], T2_list[j])
                    edge = Edge(error, (T1_list[i-1], T2_list[j-1]), (T1_list[i], T2_list[j]))
                    self.insert_edge(edge)
                error = 1
                if(T1_list[i].depth >= T2_list[j].depth):
                    edge = Edge(1, (T1_list[i-1], T2_list[j]), (T1_list[i], T2_list[j]))
                    self.insert_edge(edge)
                if(T1_list[i].depth <= T2_list[j].depth):
                    edge = Edge(1, (T1_list[i], T2_list[j-1]), (T1_list[i], T2_list[j]))
                    self.insert_edge(edge)

    def mapping(self):
        T1_list = self.T1.create_node_list()
        T2_list = self.T2.create_node_list()
        
        # L is a list of the couples of the similarity graph
        L, Weight = self.dijkstra((None, None), (T1_list[len(T1_list)-1], T2_list[len(T2_list)-1]))

        gr = Graph()
        la = list()
        for node in T1_list:
            gr.insert_vertex(node)
        for node in T2_list:
            gr.insert_vertex(node)
        
        for i in range (1,len(L)):
            tmpCouple = L[i-1]
            currentCouple = L[i]
            c_b_t0 = 0
            c_b_t1 = 0
            c_b_c0 = 0
            c_b_c1 = 0
            # if the 2 vertices are the same, there is a diagonal in the similarity graph
            if(tmpCouple[0] != None): c_b_t0 = tmpCouple[0].bijection
            if(tmpCouple[1] != None): c_b_t1 = tmpCouple[1].bijection
            if(currentCouple[0] != None): c_b_c0 = currentCouple[0].bijection
            if(currentCouple[0] != None): c_b_c1 = currentCouple[1].bijection
            
            if (( c_b_t0 +1 == c_b_c0 ) and ( c_b_t1 +1 == c_b_c1 )):
                tmpCouple_weight = Weight[i-1]
                e = Edge(tmpCouple_weight,currentCouple[0],currentCouple[1])
                gr.insert_edge(e)
                la.append(e) 
    
        return gr,la
