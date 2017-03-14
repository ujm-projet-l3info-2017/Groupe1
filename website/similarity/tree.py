class Tree():
    left = None
    right = None
    element = None

    def __init__(self, element, l, r):
        left = l
        right = r
        element = element

    def insert(self, element):
        self._insert(self, element)
        
    def _insert(self, root, element):
        if(element < self.element):
            # We go to the left
            if(self.left != None):
                # There are an element
                self.left._insert(self, root, element)
            else:
                # We can insert !
                self.left = Tree(element, None, None)
                # And we want to have a balanced tree
                self._balance(root)

        else:
            # We go to the right
            if(self.right != None):
                # There are an element
                self.right._insert(self, root, element)
            else:
                # We can insert !
                self.right = Tree(element, None, None)
                # And we want to have a balanced tree
                self._balance(root)

    def _balance(self, father):
        if(self.balance < -1 or self.balance > -1):
            self._balance_sub(father)
        else:
            if(self.left != None):
                self.left._balance(self)
            if(self.right != None):
                self.right._balance(self)
        
    def _balance_sub(self, father):
        if(self.balance == -2 and self.right.balance == -1):
            rotate_left(self, father)
        if(self.balance == 2 and self.left.blance == 1):
            rotate_right(self, father)
        if(self.balance == -2 and self.left.blance == -1):
            rotate_right_left(self, father)
        if(self.balance == -2 and self.right.blance == 1):
            rotate_left_right(self, father)

    def __str__(self):
        print(str(element)+": "+str(self.left.element)+", "+str(self.right.element))

        if(self.left != None):
            self.left.__str__()
        if(self.right != None):
            self.right.__str__()

t = Tree(0, None, None)
