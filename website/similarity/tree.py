class Tree:
    left = None
    right = None
    element = None
    balance = 0

    def __init__(self, l, r):
        self.left = l
        self.right = r

    def rotate_left(self, father):
        tree_tmp_left = self
        if(father.right == self):
            father.right = self.right
        else:
            father.left = self.right
        tree_tmp_left.right = self.left
        self.left = tree_tmp_left

    def rotate_right(self, father):
        tree_tmp_right = self
        if(father.right == self):
            father.right = self.left
        else:
            father.left = self.left
        tree_tmp_right.left = self.right
        self.right = tree_tmp_right

    def rotate_right_left(self, father):
        
            
        
