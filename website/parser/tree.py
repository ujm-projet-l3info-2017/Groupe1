class Tree():
    # We have a binary tree
    # with a left tree and a right tree
    # We have an element on the tree

    def __init__(self, element):
        self.element = element
        self.left = None
        self.right = None

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
                
    def __str__(self):
        s = str(self.element)+":"
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
