from ..tree.abstract import AbstractTree
from .lexical import SQLLexicalParser
from django.db import connection
from ..tree.avl import AVL

class TableTreeElement():
    """
    An element in a AVL to search if a table is available for a column
    """
    def __init__(self, col, tab):
        """
        Initialize an element with his column and a array which contains the SQL tables
        """
        self.col = col
        self.tab = tab
        
    def __lt__(self, other):
        """
        Introduce an order in the elements (less than)
        """
        if(isinstance(other, str)):
            return self.col < other
        if(isinstance(other, TableTreeElement)):
            return self.col < other.col

    def __eq__(self, other):
        """
        Introduce an order in the elements (equal)
        """
        if(isinstance(other, str)):
            return self.col == other
        if(isinstance(other, TableTreeElement)):
            return self.col == other.col

    def __str__(self):
        return self.col+" ("+str(self.tab)+")"
    
    def add_table(self, table):
        """
        Add a SQL table in the array
        """
        self.tab.append(table)

    def get_table(self):
        """
        Get the table in the array (if the table is unique)
        """
        if(len(self.tab) == 1):
            return self.tab[0]
        return None
    
def create_table_tree(tables):
    """
    Create the tree
    """
    tree = None
    for table in tables:
        tree = insert_table(table, tree)
    return tree

def insert_table(table, tree):
    """
    Insert a table in the tree
    """
    with connection.cursor() as cursor:
        try:
            table = table.lower()
            cursor.execute("SELECT * FROM "+table)
            # Get the columns of the table 
            column_name = [col[0].lower() for col in cursor.description]

            # Create a column

            # If there are no tree we create the first node
            if(tree == None):
                col = column_name.pop()
                tree = AVL(TableTreeElement(col, [table]))

            # Insert the column in the tree
            for col in column_name:
                if(tree[col] != None):
                    tree[col].add_table(table)
                else:
                    tree = tree.insert(TableTreeElement(col, [table]))
        except:
            pass
            # If there are a problem: Nothing !
    return tree

def modify_tree_column(table_tree, column_tree):
    """
    We modify the column in adding the table name
    """
    column = column_tree.element.lower()
    if(table_tree[column] != None and table_tree[column].get_table() != None):
        column_tree.element = table_tree[column].get_table()+"."+column
        column_tree.text = table_tree[column].get_table()+"."+column
