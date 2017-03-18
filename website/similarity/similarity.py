from tree import Tree

class Element():
    # An Element is composed of the content of the line (value) and where the content is
    # (with an array of numbers of line). 
    value = ""
    line = []
    
    def __init__(self, value, line):
        self.value = value
        self.line = line

    def __lt__(self, other):
        # We introduce the order of the element:
        # we test here if self < other

        # If other is a string 
        if(isinstance(other, str)):
            return self.value < other
        # If other is an Element
        if(isinstance(other, Element)):
            return self.value < other.value

    def __eq__(self, other):
        # We continue to introduce the order:
        # we test here the equality
        
        if(isinstance(other, str)):
            return self.value == other
        if(isinstance(other, Element)):
            return self.value == other.value

    def __str__(self):
        return self.value+"("+str(self.line)+")"
    
    def add_line(self, line):
        # If the element exists in the tree, we have to add the number of the line
        # in the array of the object
        self.line.append(line)

    def get_line(self):
        # Get the array of numbers of lines
        return self.line
    
def convert_column_tree(column):
    # Convert a column in a single tree (an AVL tree)
    tree = Tree(Element(column[0], [0]))
    for i in range(1, len(column)):
        element = tree[column[i]]
        if(element != None):
            # If the element exists, add the number of the line in the array 
            element.add_line(i)
        else:
            # If it doesn't exist, we insert the content of the line in the tree
            tree = tree.insert(Element(column[i], [i]))
    return tree

def convert_table_tree(rows, column_name):
    # Convert a table in a dictionary of trees
    table = {}
    for i in range(len(column_name)):
        column = [line[i] for line in rows]
        table[column_name[i]] = convert_column_tree(column)
    return table


#===================================================#
#                       Tests                       #
#===================================================#

column_name = ["C1", "C2", "C3", "C4"]
row = [["1", "3", "A", "B"],
       ["2", "4", "7", "D"],
       ["T", "z", "e", "T"],
       ["Z", "e", "A", "T"],
       ["hey", "12/12", "g", "SELECT *"]]
table = convert_table_tree(row, column_name)
print(table["C1"])
print(table["C2"])
print(table["C3"])
print(table["C4"])
table["C4"]["D"] = "coucou"
print(table["C4"]["D"])
