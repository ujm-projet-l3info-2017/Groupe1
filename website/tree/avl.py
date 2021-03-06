from .tree import Tree 
class AVL(Tree):

    # We have an AVL, so we have to add the balance of the tree
    def __init__(self, element):
        """
        Initialize the AVL with an element and the balance of the tree
        """
        self.element = element
        self.left = None
        self.right = None
        self.balance = 0

    def rotate_left(self, father, root):
        """
        We rotate (left) the sub tree if the tree isn't well-balanced
        """
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
        """
        We rotate (right) the sub tree if the tree isn't well-balanced
        """
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
        """
        We rotate (right-left) the sub tree if the tree isn't well-balanced
        """
        # Another case of rotation which use rotate_right and rotate_left
        root = self.right.rotate_right(self, root)
        root = self.rotate_left(father, root)
        return root

    def rotate_left_right(self, father, root):
        """
        We rotate (left-right) the sub tree if the tree isn't well-balanced
        """
        # The last case !
        root = self.left.rotate_left(self, root)
        root = self.rotate_right(father, root)
        return root

    def insert(self, element):
        """
        Insert an element in the AVL
        """
        # We call the recursive function
        return self._insert(self, element)
        
    def _insert(self, root, element):
        """
        The bis function of insert
        """
        if(element < self.element):
            # We go to the left
            if(self.left != None):
                # There are an element
                return self.left._insert(root, element)
            else:
                # We can insert !
                self.left = AVL(element)
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
                self.right = AVL(element)
                # And we want to have a balanced tree
                root = root._balance(root, root)
                return root

    def compute_balance(self):
        """
        Compute the balance of the tree
        """
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
        
    def _balance(self, father, root):
        """
        Balance the tree
        """
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
        """
        Rotate the tree according to different conditions
        """
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
        """
        Search recursively the item
        """
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
        """
        Search and set recursively the item
        """
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
