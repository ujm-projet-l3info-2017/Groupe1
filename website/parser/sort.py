def concat_0(self):
    """
    Concatenate the first node
    """
    if (self != None):
        return str(self.element)+concat(self.left)
    
def concat(self):
    """
    Concatenation of each attribute with their sons(left) and brothers(right)
    """
    if (self != None):
        return str(self.element)+concat(self.left)+concat(self.right)
    else:
        return ''
    
def brothers(self):
    """
    Count the number(size) of brothers(right) 
    """
    count = 0
    tmp = self
    while (tmp != None):
        count+=1
        tmp = tmp.right
    return count

def node(self,index):
    """
    Return the index-nth brother of self
    """
    if( index==0):
        return self
    else :
        return node(self.right,index-1)

def order(element1, element2):
    """
    Compare two elements based on lexicographic order
    """
    return(element1<element2)

def sort_element(self, size):
    """
    Bubble sort on each of self's brothers, after they are turned into strings
    """
    if (size>=2):
        for i in range (size, 1,-1):
            is_sorted = True
            for j in range (0, i-1):
                if (order(concat_0(node(self,j+1)),concat_0(node(self,j)))):
                    tmp1 = node(self,j+1).element
                    tmp2 = node(self,j+1).left
                    node(self,j+1).element = node(self,j).element
                    node(self,j+1).left = node(self,j).left
                    node(self,j).element = tmp1
                    node(self,j).left = tmp2
                    is_sorted = False
                    if (is_sorted):
                        break

def sort(self):
    #Execute bubble sort on the branch of the query tree
    if (self.get_son() != None):
        sort_element(self.get_son(),brothers(self.get_son()))
