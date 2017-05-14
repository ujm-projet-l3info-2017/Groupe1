from .tree import Tree
class AbstractTree(Tree):
    """
    The abstract tree is the tree for the parser
    """
    def __init__(self, element, text):
        """
        We initialize the tree with a text and an element
        """
        super().__init__(element)
        self.text = text
    
    def concatenate_father_son(self, son):
        """
        The concatenation of two tree (son is concatenate to the left pointer of the father)
        """
        self.left = son

    def concatenate_father_brother(self, brother):
        """
        The concatenation of two tree (brother is concatenate to the right pointer of the father)
        """
        self.right = brother

    def get_son(self):
        """
        Get the son of the tree
        """
        return self.left

    def get_brother(self):
        """
        Get the brother of the tree
        """
        return self.right
        
