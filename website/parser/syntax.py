from .lexical import *
from ..tree.abstract import AbstractTree
from .sort import *
from .bdd import *
import re

class SyntaxParser():
    """
    Create a syntaxical parser
    """
    def __init__(self, sentence):
        """
        Initialize the parser with a sentence and initialize the lexical parser
        """
        self.lexical = LexicalParser(sentence)
        self.lookahead = None
        
    def get_lookahead(self):
        """
        Get the lookahead
        """
        return self.lookahead

    def shift(self):
        """
        Shift: get the lexeme 
        """
        self.lookahead = self.lexical.get_lexeme()
        #print("lookahead: "+str(self.lookahead))

    def parse_error(self):
        """
        The parse error function
        """
        #print("parsing error")
        raise NameError("Erreur d'analyse")

    def parse(self):
        """
        The parse function which is not implemented for the general parser 
        """
        raise NotImplementedError

class SQLSyntaxParser(SyntaxParser):
    """
    SQL Parser
    """
    def __init__(self, sentence):
        """
        Initialize a SQL parser with a sentence 
        """
        self.lexical = SQLLexicalParser(sentence)
        self.select_column = []
        self.table_tree = None
        
    def parse(self):
        """
        Parse the sentence
        """
        self.shift()
        tree =  self.query_list()
        tree.compute_depth()
        tree.compute_bijection()
        return tree

    def query_list(self):
        """
        <QUERY_LIST> ::= <QUERY> <QUERY_LIST_NEXT> | opening <QUERY> closing <QUERY_LIST_NEXT>
        """
        if(self.get_lookahead() == self.lexical._opening):
            tree = AbstractTree(self.lexical._query,"")
            self.shift()
            tree_query = self.query()
            tree.concatenate_father_son(tree_query)
            if(self.get_lookahead() == self.lexical._closing):
                self.shift()
                tree_list = self.query_list_next()
                tree.concatenate_father_brother(tree_list)
                return tree
            else:
                self.parsing_error()
        else:
            tree = AbstractTree(self.lexical._query, "")
            tree_query = self.query()
            tree.concatenate_father_son(tree_query)
            tree_list = self.query_list_next()
            tree.concatenate_father_brother(tree_list)
            return tree

    def query_list_next(self):
        """
        <QUERY_LIST_NEXT> ::= [ name <QUERY_LIST> ]
        """
        if(self.get_lookahead() == self.lexical._name):
            tree = AbstractTree(self.lexical.get_text(), self.lexical.get_text())
            self.shift()
            tree_list = self.query_list()
            tree.concatenate_father_brother(tree_list)
            return tree

    def query(self):
        """
        <QUERY> ::= <SELECT_MODE> <SELECT> from <COLUMN_LIST> <QUERY_NEXT>
        """
        tree = self.select_mode()
        tree_select = self.select()
        tree.concatenate_father_son(tree_select)
        if(self.get_lookahead() == self.lexical._from):
            tree_from = AbstractTree(self.lexical._from, self.lexical.get_text())
            self.shift()
            tree_name = self.name_list()

            # Check if the table is not an admin table 
            check_table=tree_name
            while(check_table!=None):
                m = re.match(r"^auth.+|^django.+|^website.*",check_table.element)
                if(m != None):
                    return self.parse_error()
                check_table=check_table.get_brother()
            
                
            # We have to create the tree of tables
            tables = []
            tmp = tree_name
            while(tmp != None):
                # It's just the column: we have to transform the tree
                tables.append(tmp.element)
                tmp = tmp.get_brother()
                
            # We can now construct the table tree
            self.table_tree = create_table_tree(tables)

            # We can transform the column of the SELECT
            for col in self.select_column:
                modify_tree_column(self.table_tree, col)

            tree_next = self.query_next()
            tree_from.concatenate_father_son(tree_name)
            tree_from.concatenate_father_brother(tree_next)
            tree.concatenate_father_brother(tree_from)
            return tree
        else:
            return self.parse_error()

    def select_mode(self):
        """
        <SELECT_MODE> ::= select | select_distinct
        """
        if(self.get_lookahead() == self.lexical._select_distinct):
            tree_mode = AbstractTree(self.lexical._select_distinct, self.lexical.get_text())
            self.shift()
            return tree_mode
        elif(self.get_lookahead() == self.lexical._select):
            tree_mode = AbstractTree(self.lexical._select, self.lexical.get_text())
            self.shift()
            return tree_mode
        else:
            return self.parse_error()

    def select(self):
        """
        <SELECT> ::= star | <COLUMN_SELECT_LIST>
        """
        if(self.get_lookahead() == self.lexical._star):
            tree_star = AbstractTree(self.lexical._star, self.lexical.get_text())
            self.shift()
            return tree_star
        else:
            tree = self.column_select_list()
            # Insert the subtree to transform the column when we have tables
            tmp = tree
            while(tmp != None):
                if(not(re.compile("[a-zA-Z0-9]*\.[a-zA-Z0-9]*").match(tmp.text))):
                    # It's just the column: we have to transform the tree
                    self.select_column.append(tmp)
                tmp = tmp.get_brother()
            return tree

    def column(self):
        """
        <COLUMN> ::= name <COLUMN_NEXT>
        """
        if(self.get_lookahead() == self.lexical._name):
            tree = AbstractTree(self.lexical.get_text(), self.lexical.get_text())
            self.shift()
            tree_next = self.column_next()
            
            if(tree_next == None and self.table_tree != None):
                modify_tree_column(self.table_tree, tree)
            elif(tree_next != None and tree_next.element == self.lexical._dot):
                column = tree_next.get_son().element
                tree.element = tree.element+"."+column
                tree.text = tree.text+"."+column
            else:
                tree.concatenate_father_son(tree_next)
            return tree
        else:
            return self.parse_error()

    def column_next(self):
        """
        <COLUMN_NEXT> ::= [dot name | opening <COLUMN> closing]
        """
        if(self.get_lookahead() == self.lexical._dot):
            tree_dot = AbstractTree(self.lexical._dot, self.lexical.get_text())
            self.shift()
            if(self.get_lookahead() == self.lexical._name):
                tree_dot.concatenate_father_son(AbstractTree(self.lexical.get_text(), self.lexical.get_text()))
                self.shift()
                return tree_dot
            else:
                return self.parse_error()
        elif(self.get_lookahead() == self.lexical._opening):
            self.shift()
            tree = self.column()
            if(self.get_lookahead() == self.lexical._closing):
                self.shift()
                return tree
            else:
                return self.parse_error()

    def column_select_list(self):
        """
        <COLUMN_SELECT_LIST> ::= <COLUMN> <COLUMN_AS> <COLUMN_SELECT_LIST_NEXT>
        """
        tree_column = self.column()
        tree_as = self.column_as()
        tree_select = self.column_select_list_next()
        tree_column.concatenate_father_son(tree_as)
        tree_column.concatenate_father_brother(tree_select)
        return tree_column

    def column_as(self):
        """
        <COLUMN_AS> ::= [as name];
        """
        if(self.get_lookahead() == self.lexical._as):
            tree_as = AbstractTree(self.lexical._as, self.lexical.get_text())
            self.shift()
            if(self.get_lookahead() == self.lexical._name):
                tree_as.concatenate_father_son(AbstractTree(self.lexical.get_text(), self.lexical.get_text()))
                self.shift()
                return tree_as
            else:
                return self.parse_error()

    def column_select_list_next(self):
        """
        <COLUMN_SELECT_LIST_NEXT> ::= [comma <COLUMN_SELECT_LIST>]
        """
        if(self.get_lookahead() == self.lexical._comma):
            self.shift()
            tree = self.column_select_list()
            return tree

    def column_list(self):
        """
        <COLUMN_LIST> ::= <COLUMN> <COLUMN_LIST_NEXT>
        """
        tree_column = self.column()
        tree_list = self.column_list_next()
        tree_column.concatenate_father_brother(tree_list)
        return tree_column

    def column_list_next(self):
        
        if(self.get_lookahead() == self.lexical._comma):
            self.shift()
            tree = self.column_list()
            return tree
            
    def name_list(self):
        if(self.get_lookahead() == self.lexical._name):
            tree = AbstractTree(self.lexical.get_text(), self.lexical.get_text())
            self.shift()
            tree_list = self.name_list_next()
            tree.concatenate_father_brother(tree_list)
            return tree
        else:
            return self.parse_error()

    def name_list_next(self):
        if(self.get_lookahead() == self.lexical._comma):
            self.shift()
            tree = self.name_list()
            return tree

    def query_next(self):
        if(self.get_lookahead() == self.lexical._where):
            tree_where = AbstractTree(self.lexical._where, self.lexical.get_text())
            self.shift()
            tree_condition = self.condition()
            tree_group_by = self.group_by()
            tree_where.concatenate_father_son(tree_condition)
            tree_where.concatenate_father_brother(tree_group_by)
            return tree_where
        else:
            tree = self.group_by()
            return tree

    def group_by(self):
        if(self.get_lookahead() == self.lexical._group_by):
            tree_group_by = AbstractTree(self.lexical._group_by, self.lexical.get_text())
            self.shift()
            tree_column = self.column_list()

            # We have to transform the column list
            tmp = tree_column
            while(tmp != None):
                if(tmp.get_son() == None):
                    # It's just the column: we have to transform the tree
                    modify_tree_column(self.table_tree, tmp)
                tmp = tmp.get_brother()
                
            tree_having = self.having()
            tree_group_by.concatenate_father_son(tree_column)
            tree_group_by.concatenate_father_brother(tree_having)
        else:
            tree = self.having()
            return tree

    def having(self):
        if(self.get_lookahead() == self.lexical._having):
            tree_having = AbstractTree(self.lexical._having, self.lexical.get_text())
            self.shift()
            tree_condition = self.condition()
            tree_order = self.order()
            tree_having.concatenate_father_son(tree_condition)
            tree_having.concatenate_father_brother(tree_order)
            return tree_having
        else:
            tree = self.order()
            return tree

    def order(self):
        if(self.get_lookahead() == self.lexical._order_by):
            tree_order_by = AbstractTree(self.lexical._order_by, self.lexical.get_text())
            self.shift()
            tree_column = self.column_list()

            # We have to transform the column list
            tmp = tree_column
            while(tmp != None):
                if(tmp.get_son() == None):
                    # It's just the column: we have to transform the tree
                    modify_tree_column(self.table_tree, tmp)
                tmp = tmp.get_brother()
                
            tree_order_op = self.order_op()
            tree_order_by.concatenate_father_son(tree_column)
            return tree_order_by

    def order_op(self):
        if(self.get_lookahead() == self.lexical._asc):
            tree = AbstractTree(self.lexical._asc, self.lexical.get_text())
            self.shift()
            return tree
        elif(self.get_lookahead() == self.lexical._desc):
            tree = AbstractTree(self.lexical._desc, self.lexical.get_text())
            self.shift()
            return tree
        else:
            return self.parse_error()

    def condition(self):
        tree_test = self.test()
        tree_condition = self.condition_next()

        # We have to test if we have an and or an or
        if(tree_condition != None):
            tree_test.concatenate_father_brother(tree_condition.get_son())
            tree_condition.concatenate_father_son(tree_test)
            sort_from(tree_condition)
            return tree_condition
        return tree_test

    def condition_next(self):
        if(self.get_lookahead() == self.lexical._and):
            tree_and = AbstractTree(self.lexical._and, self.lexical.get_text())
            self.shift()
            tree = self.condition()
            tree_and.concatenate_father_son(tree)
            return tree_and
        elif(self.get_lookahead() == self.lexical._or):
            tree_or = AbstractTree(self.lexical._or, self.lexical.get_text())
            self.shift()
            tree = self.condition()
            tree_or.concatenate_father_son(tree)
            return tree_or

    def test(self):
        if(self.get_lookahead() == self.lexical._opening):
            self.shift()
            tree = self.condition()
            if(self.get_lookahead() == self.lexical._closing):
                self.shift()
                return tree
            else:
                return self.parse_error()
        elif(self.get_lookahead() == self.lexical._not):
            tree_not = AbstractTree(self.lexical._not, self.lexical.get_text())
            self.shift()
            tree = self.test_other()
            tree_not.concatenate_father_son(tree)
            return tree_not
        elif(self.get_lookahead() == self.lexical._like or self.get_lookahead() == self.lexical._in):
            tree = self.test_other()
            return tree
        else:
            tree_column = self.column()
            tree_op = self.op()
            tree_test_next = self.test_next()
            tree_column.concatenate_father_brother(tree_test_next)
            tree_op.concatenate_father_son(tree_column)
            if(tree_op.element == SQLLexicalParser._equal or tree_op.element == SQLLexicalParser._not_equal):
                # Sort the tree if we have an (non-)equality
                sort_from(tree_op)
            return tree_op

    def test_other(self):
        if(self.get_lookahead() == self.lexical._like):
            tree_like = AbstractTree(self.lexical._like, self.lexical.get_text())
            self.shift()
            if(self.get_lookahead() == self.lexical._exp):
                tree_like.concatenate_father_son(AbstractTree(self.lexical.get_text(), self.lexical.get_text()))
                self.shift()
                return tree_like
            else:
                return self.parse_error()
        elif(self.get_lookahead() == self.lexical._in):
            tree_in = AbstractTree(self.lexical._in, self.lexical.get_text())
            self.shift()
            if(self.get_lookahead() == self.lexical._opening):
                self.shift()
                tree = self.query_list()
                if(self.get_lookahead() == self.lexical._closing):
                    self.shift()
                    tree_in.concatenate_father_son(tree)
                    return tree_in
                else:
                    return self.parse_error()
            else:
                return self.parse_error()
        else:
            return self.parse_error()

    def test_next(self):
        if(self.get_lookahead() == self.lexical._opening):
            self.shift()
            tree = self.query_list()
            if(self.get_lookahead() == self.lexical._closing):
                self.shift()
            else:
                return self.parse_error()
        elif(self.get_lookahead() == self.lexical._quote or self.get_lookahead() == self.lexical._double_quote or self.get_lookahead() == self.lexical._number):
            tree = self.value()
        else:
            tree = self.column()
        return tree

    def op(self):
        if(self.get_lookahead() == self.lexical._equal):
            tree = AbstractTree(self.lexical._equal, self.lexical.get_text())
            self.shift()
            return tree
        elif(self.get_lookahead() == self.lexical._not_equal):
            tree = AbstractTree(self.lexical._not_equal, self.lexical.get_text())
            self.shift()
            return tree
        elif(self.get_lookahead() == self.lexical._less):
            tree = AbstractTree(self.lexical._less, self.lexical.get_text())
            self.shift()
            return tree
        elif(self.get_lookahead() == self.lexical._greater):
            tree = AbstractTree(self.lexical._greater, self.lexical.get_text())
            self.shift()
            return tree
        elif(self.get_lookahead() == self.lexical._less_e):
            tree = AbstractTree(self.lexical._less_e, self.lexical.get_text())
            self.shift()
            return tree
        elif(self.get_lookahead() == self.lexical._greater_e):
            tree = AbstractTree(self.lexical._greater_e, self.lexical.get_text())
            self.shift()
            return tree
        else:
            return self.parse_error()

    def value(self):
        if(self.get_lookahead() == self.lexical._quote):
            self.shift()
            if(self.get_lookahead() == self.lexical._name):
                tree = AbstractTree(self.lexical.get_text(), self.lexical.get_text())
                self.shift()
                if(self.get_lookahead() == self.lexical._quote):
                    self.shift()
                    return tree
                else:
                    return self.parse_error()
            else:
                return self.parse_error()
        elif(self.get_lookahead() == self.lexical._double_quote):
            self.shift()
            if(self.get_lookahead() == self.lexical._name):
                tree = AbstractTree(self.lexical.get_text(), self.lexical.get_text())
                self.shift()
                if(self.get_lookahead() == self.lexical._double_quote):
                    self.shift()
                    return tree
                else:
                    return self.parse_error()
            else:
                return self.parse_error()
        elif(self.get_lookahead() == self.lexical._number):
            tree = AbstractTree(self.lexical.get_text(), self.lexical.get_text())
            self.shift()
            return tree
        else:
            return self.parse_error()
