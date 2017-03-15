class Tree():
    left = None
    right = None
    element = None
    balance = 0

    def __init__(self, element):
        self.element = element

    def rotate_left(self, father, root):
        if(self == root):
            root = self.right
        tmp = self.right.left
        if(father != self):
            if(father.right == self):
                father.right = self.right
            else:
                father.left = self.right
        self.right.left = self
        self.right = tmp
        return root

    def rotate_right(self, father, root):
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
        root = self.right.rotate_right(self)
        root = self.rotate_left(father)
        return root

    def rotate_left_right(self, father, root):
        root = self.left.rotate_left(self)
        root = self.rotate_right(father)
        return root

    def insert(self, element):
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
        if(self.left != None):
            self.left.compute_balance()
            left_balance = self.left.height()+1
        else:
            left_balance = 0
        if(self.right != None):
            self.right.compute_balance()
            right_balance = self.right.height()+1
        else:
            right_balance = 0
        self.balance = left_balance - right_balance

    def height(self):
        if(self == None):
            return 0
        
        if(self.left != None):
            height_left = self.left.height()+1
        else:
            height_left = 0
        if(self.right != None):
            height_right = self.right.height()+1
        else:
            height_right = 0
        if(height_left > height_right):
            return height_left
        else:
            return height_right
        
    def _balance(self, father, root):
        if(self == root):
            self.compute_balance()
        if(self.left != None):
            root = self.left._balance(self, root)
        if(self.right != None):
            root = self.right._balance(self, root)

        if(self.balance < -1 or self.balance > 1):
            root = self._balance_sub(father, root)
            root.compute_balance()
        return root
        
        
    def _balance_sub(self, father, root):
        if(self.balance == -2 and self.right.balance == -1):
            root = self.rotate_left(father, root)
        elif(self.balance == 2 and self.left.balance == 1):
            root = self.rotate_right(father, root)
        elif(self.balance == -2 and (self.right.balance == 1 or self.right.balance == 0)):
            root = self.rotate_right_left(father, root)
        elif(self.balance == 2 and (self.right.balance == -1 or self.right.balance == 0)):
            root = self.rotate_left_right(father, root)
        return root

    def __getitem__(self, key):
        if(self.element == key):
            return self.element
        else:
            if(self.element < key):
                if(self.right != None):
                   return self.right.__getitem__(key)
            else:
                if(self.left != None):
                   return self.left.__getitem__(key)
            return None 

    def __setitem__(self, key, value):
        if(self.element == key):
            self.element = value
        else:
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
