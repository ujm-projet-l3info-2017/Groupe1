from ..tree.avl import AVL

GREEN = 0
ORANGE = 1
RED = 2

class Element():
    """
    An Element is composed of the content of the line (value) and where the content is
    (with an array of numbers of line). 
    """
    value = ""
    line = []
    
    def __init__(self, value, line):
        self.value = value
        self.line = line

    def __lt__(self, other):
        """
        We introduce the order of the element:
        we test here if self < other
        """
        
        # If other is a string 
        if(isinstance(other, str)):
            return self.value < other
        # If other is an Element
        if(isinstance(other, Element)):
            return self.value < other.value

    def __eq__(self, other):
        """
        We introduce the order of the element:
        we test here the equality
        """
        if(isinstance(other, str)):
            return self.value == other
        if(isinstance(other, Element)):
            return self.value == other.value

    def __str__(self):
        return str(self.value)+"("+str(self.line)+")"
    
    def add_line(self, line):
        """
        If the element exists in the tree, we have to add the number of the line
        in the array of the object
        """
        self.line.append(line)

    def exist_line(self, number):
        """
        Test if the number of the line is in the list
        """
        try:
            if(self.line.index(number) >= 0):
                return True
            return False
        except ValueError:
            return False

    def get_line(self):
        return self.line
    
def convert_column_tree(column):
    """
    Convert a column in a single tree (an AVL tree)
    """
    tree = AVL(Element(column[0], [0]))
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
    """
    Convert a table in a dictionary of trees
    """
    table = {}
    for i in range(len(column_name)):
        column = [line[i] for line in rows]
        table[column_name[i]] = convert_column_tree(column)
    return table

def compare_line(table_expected, table_result, column_expected, column_result, color_column, trees, number_line):
    """
    Compare a line in the expected table and in the user table
    """ 
    if(len(table_expected) > len(table_result)):
        count_line = [0 for i in range(len(table_expected))]
    else:
        count_line = [0 for i in range(len(table_result))]
    length_expected = len(column_result)
    color_table_row = []
    for i in range(len(column_result)):
        elem = table_result[number_line][i]
        try:
            # Use the right tree
            tree = trees[column_result[i]]
            if(tree[elem] != None):
                line = tree[elem].get_line()
                for e in line:
                    count_line[e] += 1
        except:
            # We don't have the column, so we decrement length_expected
            length_expected -= 1

    if(count_line[number_line] == length_expected and length_expected > 0):
        # the line is at the right place
        for j in range(len(table_result[number_line])):
            try:
                if(trees[column_result[j]] != None):
                    # The column exist in the tree : we had its color
                    if(color_column[j] == GREEN):
                        color_table_row.insert(j, GREEN)
                    else:
                        color_table_row.insert(j, ORANGE)
                else:
                    # If the column doesn't exist: we use the red
                    color_table_row.insert(j, RED)
            except:
                color_table_row.insert(j, RED)
        return color_table_row
    else:
        for number in count_line:
            if(number == length_expected and length_expected > 0):
                # the line isn't at the right place
                for j in range(len(table_result[number_line])):
                    try:
                        if(trees[column_result[j]] != None):
                            # The column exist in the tree : we had its color
                            color_table_row.insert(j, ORANGE)
                        else:
                            # If the column doesn't exist: we use the red
                            color_table_row.insert(j, RED)
                    except:
                        # If the column doesn't exist: we use the red
                        color_table_row.insert(j, RED)
                return color_table_row
        # the line doesn't exist
        return RED

def compare_table(table_expected, table_result, column_expected, column_result):
    """
    Color the user table
    """
    length_expected = len(column_expected)
    color_column = []
    color_table = []
    trees = convert_table_tree(table_expected, column_expected)
    # Attribute a color to a column :
    #    GREEN if it's ok
    #    ORANGE if it's not at the right place
    for i in range(len(column_result)):
        if(i < length_expected and column_expected[i] == column_result[i]):
            color_column.insert(i, GREEN)
        else:
            color_column.insert(i, ORANGE)

    for i in range(len(table_result)):
        color_table_row = compare_line(table_expected, table_result, column_expected, column_result, color_column, trees, i)
        if(color_table_row == RED):
            color_table_row = compare_column(table_expected, table_result, column_expected, column_result, color_column, trees, i)
        color_table.insert(i, color_table_row)
    return color_table
                 
def compare_column(table_expected, table_result, column_expected, column_result, color_column, trees, number_line):
    """
    Attribute a color at each cell of the table
    """
    color_table_row = []
    for j in range(len(column_result)):
        elem = table_result[number_line][j]
        try:
            # Use the right tree
            tree = trees[column_result[j]]
            # Check if the element exist in the tree
            # if tree[elem] doesn't exist, we go to the exception
            if(tree[elem] != None and tree[elem].exist_line(number_line)):
                if(color_column[j] == GREEN):
                    color_table_row.insert(j, GREEN)
                else:
                    color_table_row.insert(j, ORANGE)
            else:
                color_table_row.insert(j, RED)
        except KeyError:
            # The column doesn't exist
            color_table_row.insert(j, RED)
            color_column[j] = RED
    return color_table_row
