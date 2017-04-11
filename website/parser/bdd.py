from abstract import AbstractTree
from lexical import SQLLexicalParser
#from django.db import connection
from avl import AVL

class TableTreeElement():

    def __init__(self, col, tab):
        self.col = col
        self.tab = tab
        
    def __lt__(self, other):
        if(isinstance(other, str)):
            return self.col < other
        if(isinstance(other, TableTreeElement)):
            return self.col < other.col

    def __eq__(self, other):
        if(isinstance(other, str)):
            return self.col == other
        if(isinstance(other, TableTreeElement)):
            return self.col == other.col

    def __str__(self):
        return self.col+" ("+str(self.tab)+")"
    
    def add_table(self, table):
        self.tab.append(table)

    def get_table(self):
        if(len(self.tab) == 1):
            return self.tab[0]
        return None
    
def create_table_tree(tables):
    tree = None
    for table in tables:
        tree = insert_table(table, tree)
    return tree

def insert_table(table, tree):
    #with connection.cursor() as cursor:
     #   try:
            #cursor.execute("SELECT * FROM "+table)
            #column_name = [col[0] for col in cursor.description]
    column_name = ["x", "y", "z"]

    if(tree == None):
        col = column_name.pop()
        tree = AVL(TableTreeElement(col, [table]))
    
    for col in column_name:
        if(tree[col] != None):
            tree[col].add_table(table)
        else:
            tree = tree.insert(TableTreeElement(col, [table]))
      #  except:
       #     pass
            # Nothing !
    return tree

def modify_tree_column(table_tree, column_tree):
    column = column_tree.element
    if(table_tree[column] != None and table_tree[column].get_table() != None):
        column_tree.element = table_tree[column].get_table()
        tree_dot = AbstractTree(SQLLexicalParser._dot)
        tree_column = AbstractTree(column)
        tree_dot.concatenate_father_son(tree_column)
        column_tree.concatenate_father_son(tree_dot)