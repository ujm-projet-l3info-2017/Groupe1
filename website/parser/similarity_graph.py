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
        print(T1_list)
        print(T2_list)

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

        s = ""
        for i in range(1, len(T1_list)):
            s += str(T1_list[i].text)+" "
        print(s)
        s= ""
        for i in range(1, len(T2_list)):
            s += str(T2_list[i].text)+" "
        print(s)
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
                print("v"+str(c_b_c0)+", w"+str(c_b_c1)+", weight "+str(tmpCouple_weight))
                e = Edge(tmpCouple_weight,currentCouple[0],currentCouple[1])
                gr.insert_edge(e)
                la.append(e) 
    
        return gr,la

class Mapping():

    def __init__(self, tree_expected, tree_user):
        self.tree_expected = tree_expected
        self.tree_user = tree_user
        self.sim = SimilarityGraph(self.tree_expected, self.tree_user)
        self.sim.create_graph()
        _, self.edge_list = self.sim.mapping()
    
    def compare_added(self, l_t1, l_t2):
        l_t1_non_sorted = l_t1.copy()
        l_t2_non_sorted = l_t2.copy()
        l_t1.sort()
        l_t2.sort()
 
        while(l_t1 and l_t2):
            if(l_t1[0] < l_t2[0]):
                e = l_t1.pop(0)
                l_t1_non_sorted.remove(e)
                print(str(e.text)+" must be added")
            elif(l_t1[0] > l_t2[0]):
                e = l_t2.pop(0)
                l_t2_non_sorted.remove(e)
                print(str(e.text)+" must be removed")
            else:
                e = l_t1.pop(0)
                e = l_t2.pop(0)

        while(l_t1):
            e = l_t1.pop(0)
            l_t1_non_sorted.remove(e)
            print(str(e.text)+" must be added")
        while(l_t2):
            e = l_t2.pop(0)
            l_t2_non_sorted.remove(e)
            print(str(e.text)+" must be removed")

        while(l_t1_non_sorted and l_t2_non_sorted):
            e1 = l_t1_non_sorted.pop(0)
            e2 = l_t2_non_sorted.pop(0)
            if(e1 != e2):
                print(str(e1.text)+" must be at the right order")

    def compare(self):
        
        T1_list = self.tree_expected.create_node_list()
        T2_list = self.tree_user.create_node_list()
        l_t1 = list()
        l_t2 = list()
        
        for i in range (0 , len(self.edge_list)):
            edge = self.edge_list[i]
            edge_i = edge.start.bijection
            edge_j = edge.end.bijection

            if(i != 0):
                edge_prec = self.edge_list[i-1]
                offset_i = edge.start.bijection - edge_prec.start.bijection
                offset_j = edge.end.bijection - edge_prec.end.bijection
            else:
                offset_i = 1
                offset_j = 1

            if(offset_i == 1 and offset_j == 1 and edge.weight == 0):
                # if there are a mapping and no errors
                print("Sim: "+str(edge.start.text))
            elif(offset_i == 1 and offset_j == 1 and edge.weight == 1):
                # if there are a mapping and but errors
                l_t1.append(edge.start)
                l_t2.append(edge.end)
            else:
                if(offset_i > offset_j):
                    # The user must add elements (there are less elements in his query)
                    for j in range(edge.start.bijection-offset_i+1, edge.start.bijection):
                        l_t1.append(T1_list[j])

                elif(offset_i < offset_j):
                    for j in range(edge.end.bijection-offset_j+1, edge.end.bijection):
                        l_t2.append(T2_list[j])
                self.compare_added(l_t1, l_t2)


        for j in range(edge.start.bijection-offset_i+1, len(T1_list)):
            l_t1.append(T1_list[j])
        for j in range(edge.end.bijection-offset_j+1, len(T2_list)):
            l_t2.append(T2_list[j])
        self.compare_added(l_t1, l_t2)
