from ..graph.similarity_graph import SimilarityGraph
from ..parser.lexical import SQLLexicalParser

class Mapping():

    def __init__(self, tree_expected, tree_user):
        self.hint = []
        self.tree_expected = tree_expected
        self.tree_user = tree_user
        self.sim = SimilarityGraph(self.tree_expected, self.tree_user)
        self.sim.create_graph()
        _, self.edge_list = self.sim.mapping()


    def add_hint_added(self, join):
        for sentence in join:
            h = ""
            for tree in sentence:
                h += tree.text+" "
            self.hint.append("<b>"+h+"</b>doit etre ajoute")

    def add_hint_removed(self, join):
        for sentence in join:
            h = ""
            for tree in sentence:
                h += tree.text+" "
            self.hint.append("<b>"+h+"</b>doit etre supprime")
        
    def sort_tree_element(self, l):        
        for i in range (len(l)-1, 1,-1):
            for j in range (0, i-1):
                if str(l[j+1].element) < str(l[j].element):
                    tmp = l[j+1]
                    l[j+1] = l[j]
                    l[j] = tmp

    def join_tree_element(self, l):
        join = list()
        while(l):
            max_len = -float("inf")
            max_sub = None
            for e in l:
                sub = list()
                self.join_tree_element_bis(l, e, sub)
                if(len(sub) > max_len):
                    max_sub = sub
                    max_len = len(sub)

            for e_sub in max_sub:
                l.remove(e_sub)
            join.append(max_sub)
        return join
                
    def join_tree_op_bis(self, l, e, sub):
        find_left = False
        find_left_right = False
        if(e.left != None and (e.left.element != SQLLexicalParser._equal and e.left.element != SQLLexicalParser._not_equal and e.left.element != SQLLexicalParser._less_e and e.left.element != SQLLexicalParser._greater_e and e.left.element != SQLLexicalParser._less and e.left.element != SQLLexicalParser._greater)):
            find_left = True
        if(e.left and e.left.right != None and (e.left.right.element != SQLLexicalParser._equal and e.left.right.element != SQLLexicalParser._not_equal and e.left.right.element != SQLLexicalParser._less_e and e.left.right.element != SQLLexicalParser._greater_e and e.left.right.element != SQLLexicalParser._less and e.left.right.element != SQLLexicalParser._greater)):
            find_left_right = True

        if(find_left):
            if e.left in l:
                sub.append(e.left)
        sub.append(e)
        if(find_left_right):
            if e.left.right in l:
                sub.append(e.left.right)
            
    def join_tree_element_bis(self, l, e, sub):
        if(e.element == SQLLexicalParser._equal or e.element == SQLLexicalParser._not_equal or e.element == SQLLexicalParser._less_e or e.element == SQLLexicalParser._greater_e or e.element == SQLLexicalParser._less or e.element == SQLLexicalParser._greater):
            self.join_tree_op_bis(l, e, sub)
        else:
            sub.append(e)
    
    def compare_added(self, l_t1, l_t2):
        l_added = list()
        l_removed = list()
        l_t1_non_sorted = l_t1.copy()
        l_t2_non_sorted = l_t2.copy()
        self.sort_tree_element(l_t1)
        self.sort_tree_element(l_t2)

        while(l_t1 and l_t2):
            if(str(l_t1[0].element) < str(l_t2[0].element)):
                e = l_t1.pop(0)
                l_t1_non_sorted.remove(e)
                l_added.append(e)
            elif(str(l_t1[0].element) > str(l_t2[0].element)):
                e = l_t2.pop(0)
                l_t2_non_sorted.remove(e)
                l_removed.append(e)
            else:
                e = l_t1.pop(0)
                e = l_t2.pop(0)

        while(l_t1):
            e = l_t1.pop(0)
            l_t1_non_sorted.remove(e)
            l_added.append(e)
        while(l_t2):
            e = l_t2.pop(0)
            l_t2_non_sorted.remove(e)
            l_removed.append(e)

        while(l_t1_non_sorted and l_t2_non_sorted):
            e1 = l_t1_non_sorted.pop(0)
            e2 = l_t2_non_sorted.pop(0)
            if(str(e1.element) != str(e2.element)):
                self.hint.append(str(e1.text)+" doit etre a la bonne place")

        join_added = self.join_tree_element(l_added)
        join_removed = self.join_tree_element(l_removed)
        self.add_hint_added(join_added)
        self.add_hint_removed(join_removed)

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
                # It's similar
                pass
            elif(offset_i == 1 and offset_j == 1 and edge.weight == 1):
                # if there are a mapping and but errors
                # The two elements are mapped together but are not similar
                l_t1.append(edge.start)
                l_t2.append(edge.end)
            else:
                if(edge.weight == 0):
                    # It's similar
                    pass
                else:
                    # The two elements are mapped together but are not similar
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
