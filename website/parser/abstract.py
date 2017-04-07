from tree import Tree
class AbstractTree(Tree):

    def concatenate_father_son(self, son):
        self.left = son

    def concatenate_father_brother(self, brother):
        self.right = brother
