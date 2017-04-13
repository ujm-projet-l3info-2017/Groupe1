from graphe import Graph
from graphe import Edge
import tree

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
        T1_list[0] = None
        T2_list[0] = None

        for i in range(1, len(T1_list)):
            for j in range(1, len(T2_list)):
                if(T1_list[i].depth == T2_list[j].depth):
                    error = self.get_error(T1_list[i], T2_list[j])
                    edge = Edge(error, (T1_list[i-1], T2_list[j-1]), (T1_list[i], T2_list[j]))
                    self.insert_edge(edge)
                error = 1
                if(T1_list[i].depth >= T2_list[j].depth):
                    edge = Edge(1, (T1_list[i-1], T2_list[j-1]), (T1_list[i], T2_list[j-1]))
                    self.insert_edge(edge)
                if(T1_list[i].depth <= T2_list[j].depth):
                    edge = Edge(1, (T1_list[i-1], T2_list[j-1]), (T1_list[i-1], T2_list[j]))
                    self.insert_edge(edge)

    def mapping(self):
        T1_list = self.T1.create_node_list()
        T2_list = self.T2.create_node_list()
        
        # L is a list of the couples of the similarity graph
        L = self.dijkstra((None, None), (T1_list[len(T1_list)-1], T2_list[len(T2_list)-1]))

        s = ""
        for i in range(1, len(T1_list)):
            s += str(T1_list[i].element)+" "
        print(s)
        s= ""
        for i in range(1, len(T2_list)):
            s += str(T2_list[i].element)+" "
        print(s)
        print("T1: "+str(T1_list[6].element))
        print("T2: "+str(T2_list[4].element))
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
                e = Edge(0,currentCouple[0],currentCouple[1])
                gr.insert_edge(e)
                la.append(e) 

    
                print("v"+str(c_b_c0)+", w"+str(c_b_c1))
        return gr,la

