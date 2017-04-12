import graphe
import tree
class SimilarityGraph(Graph):
    def __init__(self, T1, T2):
        self.T1 = T1
        self.T2 = T2

    def get_error(self, T1, T2):
        if(T1.element() == T2.element()):
            return 1
        return 0

    def create_graph(self):
        T1_list = T1.create_node_list()
        T2_list = T2.create_node_list()
        T1_list[0] = None
        T2_list[0] = None

        # The average complexity is O(1)
        # and we insert in the right order ! It's OK ! 
        for T1_key in T1_list.keys():
            for T2_key in T2_list.keys():
                if(T1_list[T1_key].depth() == T2_list[T2_key].depth()):
                    error = self.get_error(T1_list[T1_key], T2_list[T2_key])
                    self.insert_edge(error, (T1_list[T1_key-1], T2_list[T2_key-1]), (T1_list[T1_key], T2_list[T2_key]))
                error = 1
                if(T1_list[T1_key].depth() >= T2_list[T2_key].depth()):
                    self.insert_edge(error, (T1_list[T1_key-1], T2_list[T2_key-1]), (T1_list[T1_key], T2_list[T2_key-1]))
                if(T1_list[T1_key].depth() <= T2_list[T2_key].depth()):
                    self.insert_edge(error, (T1_list[T1_key-1], T2_list[T2_key-1]), (T1_list[T1_key-1], T2_list[T2_key]))

def mapping(L ):
    # L is a list of the couples of the similarity graph
    gr = Graph()
    tmpCouple=L[0]
    for i in range (1,len(L)-1):
        currentCouple = L[i]
        # if the 2 vertices are the same, there is a diagonal in the similarity graph
        c_b_t0 = compute_bijection(tmpCouple[0])
        c_b_t1 = compute_bijection(tmpCouple[1])
        c_b_c0 = compute_bijection(currentCouple[0])
        c_b_c1 = compute_bijection(currentCouple[1])
        if (( c_b_t0 +1 == c_b_c0 ) and ( c_b_t1 +1 == c_b_c1 )):
            gr.insert_edge(Edge(0,currentCouple[0],currentCouple[1]))
    return gr
