class Tree():
    left = None
    right = None
    element = None
    balance = 0

    def __init__(self, element):
        self.element = element

    def rotate_left(self, father):
        tmp = self.right.left
        if(father != self):
            if(father.right == self):
                father.right = self.right
            else:
                father.left = self.right
        self.right.left = self
        self.right = tmp

    def rotate_right(self, father):
        tmp = self.left.right
        if(father.right == self):
            father.right = self.left
        else:
            father.left = self.left
        self.left.right = self
        self.left = tmp

    def rotate_right_left(self, father):
        self.right.rotate_right(self)
        self.rotate_left(father)

    def rotate_left_right(self, father):
        self.left.rotate_left(self)
        self.rotate_right(father)


    def insert(self, element):
        self._insert(self, element)
        
    def _insert(self, root, element):
        if(element < self.element):
            # We go to the left
            if(self.left != None):
                # There are an element
                self.left._insert(root, element)
            else:
                # We can insert !
                self.left = Tree(element)
                # And we want to have a balanced tree
                root.compute_balance()
                root._balance(root)
                print("--")

        else:
            # We go to the right
            if(self.right != None):
                # There are an element
                self.right._insert(root, element)
            else:
                # We can insert !
                self.right = Tree(element)
                # And we want to have a balanced tree
                root.compute_balance()
                root._balance(root)

    def compute_balance(self):
        if(self.left != None):
            self.left.compute_balance()
            left_balance = abs(self.left.balance)+1
        else:
            left_balance = 0
        if(self.right != None):
            self.right.compute_balance()
            right_balance = abs(self.right.balance)+1
        else:
            right_balance = 0
        self.balance = left_balance - right_balance


        
    def _balance(self, father):
        print(self)
        print("balance: "+str(self.balance))
        if(self.balance < -1 or self.balance > 1):
            self._balance_sub(father)
        else:
            if(self.left != None):
                self.left._balance(self)
            if(self.right != None):
                self.right._balance(self)
        
    def _balance_sub(self, father):
        if(self.balance == -2 and self.right.balance == -1):
            print("rotate_left")
            self.rotate_left(father)
        elif(self.balance == 2 and self.left.balance == 1):
            print("rotate_right")
            self.rotate_right(father)
        elif(self.balance == -2 and self.left.balance == -1):
            print("rotate_right_left")
            self.rotate_right_left(father)
        elif(self.balance == -2 and self.right.balance == 1):
            print("rotate_left_right")
            self.rotate_left_right(father)

    def __str__(self):
        s = str(self.element)+"("+str(self.balance)+"): "
        if(self.left != None):
            s += "g="+str(self.left.element)
        if(self.right != None):
            s += "d="+str(self.right.element)+"\n"
        
        
        if(self.left != None):
            s += self.left.__str__()
        if(self.right != None):
            s += self.right.__str__()
        return s

t = Tree(1)
t.insert(2)
t.insert(3)
print(t)
