class Tree():
    # We have a binary tree
    # with a left tree and a right tree
    left = None
    right = None
    # We have an element on the tree
    element = None
    # We have an AVL, so we have to add the balance of the tree
    balance = 0

    def __init__(self, element):
        self.element = element

    def rotate_left(self, father, root):
        # We rotate the sub tree if the tree isn't well-balanced

        # If we rotate on the root, we have to change
        # the root obviously ...
        if(self == root):
            root = self.right
        # We memorize the last pointer
        tmp = self.right.left
        # We have to change the child of the father ...
        if(father != self):
            if(father.right == self):
                father.right = self.right
            else:
                father.left = self.right
        # And we finish to rotate !
        self.right.left = self
        self.right = tmp
        return root

    def rotate_right(self, father, root):
        # It's exactly the same thing as rotate_left
        if(self == root):
            root = self.left
        tmp = self.left.right
        if(father.right == self):
            father.right = self.left
        else:
            father.left = self.left
        self.left.right = self
        self.left = tmp
        return root

    def rotate_right_left(self, father, root):
        # Another case of rotation which use rotate_right and rotate_left
        root = self.right.rotate_right(self, root)
        root = self.rotate_left(father, root)
        return root

    def rotate_left_right(self, father, root):
        # The last case !
        root = self.left.rotate_left(self, root)
        root = self.rotate_right(father, root)
        return root

    def insert(self, element):
        # We call the recursive function
        return self._insert(self, element)
        
    def _insert(self, root, element):
        if(element < self.element):
            # We go to the left
            if(self.left != None):
                # There are an element
                return self.left._insert(root, element)
            else:
                # We can insert !
                self.left = Tree(element)
                # And we want to have a balanced tree
                root = root._balance(root, root)
                return root

        else:
            # We go to the right
            if(self.right != None):
                # There are an element
                return self.right._insert(root, element)
            else:
                # We can insert !
                self.right = Tree(element)
                # And we want to have a balanced tree
                root = root._balance(root, root)
                return root

    def compute_balance(self):
        # If the left sub-tree exists, we compute the balance 
        if(self.left != None):
            self.left.compute_balance()
            # And we add 1 to the height !
            left_balance = self.left.height()+1
        else:
            # Otherwise, the balance is 0
            left_balance = 0
        # It's the same thing for the right
        if(self.right != None):
            self.right.compute_balance()
            right_balance = self.right.height()+1
        else:
            right_balance = 0
        # The balance of the current element is ...
        self.balance = left_balance - right_balance

    def height(self):
        # If the tree is empty, the height will be 0
        if(self == None):
            return 0

        # The maximal height of the current element at the left is
        # the maximal height of the left sub-tree + 1
        if(self.left != None):
            height_left = self.left.height()+1
        else:
            # If the left doesn't exist, the height is 0
            height_left = 0
        # It's the same thing for the height at the right
        if(self.right != None):
            height_right = self.right.height()+1
        else:
            height_right = 0
        # And we take the maximal height between the left and the right
        if(height_left > height_right):
            return height_left
        else:
            return height_right
        
    def _balance(self, father, root):
        # We will balance the tree !

        # If we are at the root, we compute the balance of the entire tree
        if(self == root):
            self.compute_balance()
        # And we balance the tree recursively
        if(self.left != None):
            root = self.left._balance(self, root)
        if(self.right != None):
            root = self.right._balance(self, root)

        # If the tree isn't well-balanced
        if(self.balance < -1 or self.balance > 1):
            # We rotate the tree
            root = self._balance_sub(father, root)
            # And we compute the balance of the entire tree
            root.compute_balance()
        return root
        
        
    def _balance_sub(self, father, root):
        # We rotate the tree according to different conditions ...
        if(self.balance == -2 and self.right.balance == -1):
            root = self.rotate_left(father, root)
        elif(self.balance == 2 and self.left.balance == 1):
            root = self.rotate_right(father, root)
        elif(self.balance == -2 and (self.right.balance == 1 or self.right.balance == 0)):
            root = self.rotate_right_left(father, root)
        elif(self.balance == 2 and (self.left.balance == -1 or self.left.balance == 0)):
            root = self.rotate_left_right(father, root)
        return root

    def __getitem__(self, key):
        # We search recursively the item ...

        # If the item exists, we return it ! 
        if(self.element == key):
            return self.element
        else:
            # Otherwise, the search at the left or at the right
            # according to the order
            if(self.element < key):
                if(self.right != None):
                   return self.right.__getitem__(key)
            else:
                if(self.left != None):
                   return self.left.__getitem__(key)
            return None 

    def __setitem__(self, key, value):
        # If we have the element, we can modify the value
        if(self.element == key):
            self.element = value
        else:
            # Otherwise, the search at the left or at the right
            # according to the order
            if(self.element < key):
                if(self.right != None):
                    self.right.__setitem__(key)
            else:
                if(self.left != None):
                    self.left.__setitem__(key)
                
    def __str__(self):
        s = str(self.element)+"("+str(self.balance)+"):"
        if(self.left != None):
            s += " g="+str(self.left.element)
        if(self.right != None):
            s += " d="+str(self.right.element)
        s += "\n"
        
        if(self.left != None):
            s += self.left.__str__()
        if(self.right != None):
            s += self.right.__str__()
        return s
