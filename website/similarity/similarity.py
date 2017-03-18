from tree import Tree

class Element():
    value = ""
    line = []
    
    def __init__(self, value, line):
        self.value = value
        self.line = line

    def __lt__(self, other):
        if(isinstance(other, str)):
            return self.value < other
        if(isinstance(other, Element)):
            return self.value < other.value

    def __eq__(self, other):
        if(isinstance(other, str)):
            return self.value == other
        if(isinstance(other, Element)):
            return self.value == other.value

    def __str__(self):
        return self.value+"("+str(self.line)+")"
    def add_line(self, line):
        self.line.append(line)

    def get_line(self):
        return self.line
    
def convert_column_tree(column):
    tree = Tree(Element(column[0], [0]))
    for i in range(1, len(column)):
        element = tree[column[i]]
        if(element != None):
            element.add_line(i)
        else:
            tree = tree.insert(Element(column[i], [i]))
    return tree

def convert_table_tree(row, column_name):
    table = {}
    for i in range(len(column_name)):
        column = [line[i] for line in row]
        table[column_name[i]] = convert_column_tree(column)
    return table

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
