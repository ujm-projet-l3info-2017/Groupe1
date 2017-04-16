from ..graph.similarity_graph import SimilarityGraph

class Mapping():

    def __init__(self, tree_expected, tree_user):
        self.hint = []
        self.tree_expected = tree_expected
        self.tree_user = tree_user
        self.sim = SimilarityGraph(self.tree_expected, self.tree_user)
        self.sim.create_graph()
        _, self.edge_list = self.sim.mapping()


    def sort_tree_element(self, l):        
        for i in range (len(l)-1, 1,-1):
            for j in range (0, i-1):
                if str(l[j+1].element) < str(l[j].element):
                    tmp = l[j+1]
                    l[j+1] = l[j]
                    l[j] = tmp

                
    def compare_added(self, l_t1, l_t2):
        l_t1_non_sorted = l_t1.copy()
        l_t2_non_sorted = l_t2.copy()
        self.sort_tree_element(l_t1)
        self.sort_tree_element(l_t2)

        while(l_t1 and l_t2):
            if(str(l_t1[0].element) < str(l_t2[0].element)):
                e = l_t1.pop(0)
                l_t1_non_sorted.remove(e)
                self.hint.append(str(e.text)+" must be added")
            elif(str(l_t1[0].element) > str(l_t2[0].element)):
                e = l_t2.pop(0)
                l_t2_non_sorted.remove(e)
                self.hint.append(str(e.text)+" must be removed")
            else:
                e = l_t1.pop(0)
                e = l_t2.pop(0)

        while(l_t1):
            e = l_t1.pop(0)
            l_t1_non_sorted.remove(e)
            self.hint.append(str(e.text)+" must be added")
        while(l_t2):
            e = l_t2.pop(0)
            l_t2_non_sorted.remove(e)
            self.hint.append(str(e.text)+" must be removed")

        while(l_t1_non_sorted and l_t2_non_sorted):
            e1 = l_t1_non_sorted.pop(0)
            e2 = l_t2_non_sorted.pop(0)
            if(str(e1.element) != str(e2.element)):
                self.hint.append(str(e1.text)+" must be at the right order")

    def compare(self):
        T1_list = self.tree_expected.create_node_list()
        T2_list = self.tree_user.create_node_list()
        l_t1 = list()
        l_t2 = list()

        s = ""
        for t in T1_list:
            if(t != None):
                s += str(t.text)+" "
        print(s)
        s = ""
        for t in T2_list:
            if(t != None):
                s += str(t.text)+" "
        print(s)

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
                self.hint.append("Sim: "+str(edge.start.text))
            elif(offset_i == 1 and offset_j == 1 and edge.weight == 1):
                # if there are a mapping and but errors
                self.hint.append("Non-Sim: "+str(edge.start.text)+" - "+str(edge.end.text))
                l_t1.append(edge.start)
                l_t2.append(edge.end)
            else:
                if(edge.weight == 0):
                    self.hint.append("Sim: "+str(edge.start.text))
                else:
                    self.hint.append("Non-Sim: "+str(edge.start.text)+" - "+str(edge.end.text))
                    l_t1.append(edge.start)
                    l_t2.append(edge.end)

                
                # We must add the elements between the elements mapped
                for j in range(edge.start.bijection-offset_i+1, edge.start.bijection):
                    l_t1.append(T1_list[j])

                for j in range(edge.end.bijection-offset_j+1, edge.end.bijection):
                    l_t2.append(T2_list[j])


        if(len(self.edge_list) > 0):
            for j in range(edge_i+1, len(T1_list)):
                l_t1.append(T1_list[j])
            for j in range(edge_j+1, len(T2_list)):
                l_t2.append(T2_list[j])
        self.compare_added(l_t1, l_t2)
