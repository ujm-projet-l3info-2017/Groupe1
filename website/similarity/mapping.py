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

    # Add hints which are in the list joined
    def add_hint_added(self, join):
        for sentence in join:
            h = ""
            for tree in sentence:
                h += tree.text+" "
            self.hint.append("<b>"+h+"</b>doit etre ajoute")

    # Add hints which are in the list joined
    def add_hint_removed(self, join):
        for sentence in join:
            h = ""
            for tree in sentence:
                h += tree.text+" "
            self.hint.append("<b>"+h+"</b>doit etre supprime")

    # Sort the tree list with the elements (Bubble sort)
    def sort_tree_element(self, l):        
        for i in range (len(l)-1, 0,-1):
            for j in range (0, i):
                if str(l[j+1].element) < str(l[j].element):
                    tmp = l[j+1]
                    l[j+1] = l[j]
                    l[j] = tmp
                elif str(l[j+1].element) == str(l[j].element) and str(l[j+1].text) < str(l[j].text):
                    tmp = l[j+1]
                    l[j+1] = l[j]
                    l[j] = tmp

    # Sort the tree list with the bijection
    def sort_tree_bijection(self, l):
        for i in range (len(l)-1, 0,-1):
            for j in range (0, i):
                if l[j+1].bijection < l[j].bijection:
                    tmp = l[j+1]
                    l[j+1] = l[j]
                    l[j] = tmp

    # Remove an element in the tree list in comparing the element 
    def remove_tree_element(self, l, e):
        for e_l in l:
            if str(e_l.element) == str(e.element) and str(e_l.text) == str(e.text):
                l.remove(e_l)

    # Join some elements to improve the printing 
    def join_tree_element(self, l):
        join = list()
        # We take the longer join in the list
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

    # We join some elements after the WHERE
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

     # We join in comparing the element in the tree list
    def join_tree_element_bis(self, l, e, sub):
        if(e.element == SQLLexicalParser._equal or e.element == SQLLexicalParser._not_equal or e.element == SQLLexicalParser._less_e or e.element == SQLLexicalParser._greater_e or e.element == SQLLexicalParser._less or e.element == SQLLexicalParser._greater):
            self.join_tree_op_bis(l, e, sub)
        else:
            sub.append(e)

    # We compare elements which are added, removed and swapped
    def compare_added(self, l_t1, l_t2):
        l_added = list()
        l_removed = list()
        # We copy l_t1 and l_t2 to compare if elements are swapped 
        l_t1_non_sorted = l_t1.copy()
        l_t2_non_sorted = l_t2.copy()
        # We sort elements with its bijection
        self.sort_tree_bijection(l_t1_non_sorted)
        self.sort_tree_bijection(l_t2_non_sorted)

        # We sort the original lists in comparing elements
        self.sort_tree_element(l_t1)
        self.sort_tree_element(l_t2)
        
        # Then we can verify if an element was added or removed
        while(l_t1 and l_t2):
            if(str(l_t1[0].element) < str(l_t2[0].element)):
                # The element was added
                e = l_t1.pop(0)
                # We don't have to verify if this element was swapped ...
                self.remove_tree_element(l_t1_non_sorted, e)
                l_added.append(e)
            elif(str(l_t1[0].element) > str(l_t2[0].element)):
                # The element was removed
                e = l_t2.pop(0)
                # We don't have to verify if this element was swapped ...
                self.remove_tree_element(l_t2_non_sorted, e)
                l_removed.append(e)
            else:
                # If the element are the same we have to compare with the text inside
                if((str(l_t1[0].text) < str(l_t2[0].text))):
                    # The element was added
                    e = l_t1.pop(0)
                    self.remove_tree_element(l_t1_non_sorted, e)
                    l_added.append(e)
                elif(str(l_t1[0].text) > str(l_t2[0].text)):
                    # The element was removed
                    e = l_t2.pop(0)
                    self.remove_tree_element(l_t2_non_sorted, e)
                    l_removed.append(e)
                else:
                    # The element are strictly the same !
                    # We have to verify if the two elements are swapped
                    e = l_t1.pop(0)
                    e = l_t2.pop(0)
                    
        while(l_t1):
            # The element was added
            e = l_t1.pop(0)
            self.remove_tree_element(l_t1_non_sorted, e)
            l_added.append(e)
        while(l_t2):
            # The element was removed
            e = l_t2.pop(0)
            self.remove_tree_element(l_t2_non_sorted, e)
            l_removed.append(e)

        # We verify if the elements are swapped or not !
        while(l_t1_non_sorted and l_t2_non_sorted):
            e1 = l_t1_non_sorted.pop(0)
            e2 = l_t2_non_sorted.pop(0)
            if(str(e1.element) != str(e2.element)):
                self.hint.append("<b>"+str(e1.text)+"</b> doit etre a la bonne place")

        # We join the elements in l_added and in l_removed
        join_added = self.join_tree_element(l_added)
        join_removed = self.join_tree_element(l_removed)
        # And we add the hints
        self.add_hint_added(join_added)
        self.add_hint_removed(join_removed)

    # We compare the mapping !
    def compare(self):
        # We create the list of the tree expected and the user tree
        T1_list = self.tree_expected.create_node_list()
        T2_list = self.tree_user.create_node_list()
        l_t1 = list()
        l_t2 = list()

        # For all egde 
        for i in range (0 , len(self.edge_list)):
            edge = self.edge_list[i]
            edge_i = edge.start.bijection
            edge_j = edge.end.bijection

            # We case for the first element ....
            if(i != 0):
                edge_prec = self.edge_list[i-1]
                offset_i = edge.start.bijection - edge_prec.start.bijection
                offset_j = edge.end.bijection - edge_prec.end.bijection
            else:
                offset_i = 1
                offset_j = 1

            if(offset_i == 1 and offset_j == 1 and edge.weight == 0):
                # Ff there are a mapping and no errors
                # It's similar
                pass
            elif(offset_i == 1 and offset_j == 1 and edge.weight == 1):
                # Ff there are a mapping and but errors
                # The two elements are mapped together but are not similar
                # So we have to add this two elements in the tree list
                if edge.start not in l_t1:
                    l_t1.append(edge.start)
                if edge.end not in l_t2:
                    l_t2.append(edge.end)
            else:
                # If there are errors between the edges
                # We must add the elements between the elements mapped
                for j in range(edge.start.bijection-offset_i, edge.start.bijection):
                    if T1_list[j] not in l_t1:
                        l_t1.append(T1_list[j])

                for j in range(edge.end.bijection-offset_j, edge.end.bijection):
                    if T2_list[j] not in l_t2:
                        l_t2.append(T2_list[j])

        # We have to compare the elements behind the last element mapped
        if(len(self.edge_list) > 0):
            for j in range(edge_i, len(T1_list)):
                if T1_list[j] not in l_t1:
                    l_t1.append(T1_list[j])
                    
            for j in range(edge_j, len(T2_list)):
                if T2_list[j] not in l_t2:
                    l_t2.append(T2_list[j])
        self.compare_added(l_t1, l_t2)
