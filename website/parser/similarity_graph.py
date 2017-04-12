import graphe
import tree
class SimilarityGraph(Graph):
    def __init__(self, T1, T2):
        
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
