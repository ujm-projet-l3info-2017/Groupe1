import graphe

class SimilarityGraph(Graph):
    def __init__(self, T1, T2):
        self.T1 = T1
        self.T2 = T2

    def get_error(self, T1, T2):
        if(T1.element() == T2.element()):
            return 1
        return 0
