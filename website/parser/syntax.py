from lexical import *
from abstract import AbstractTree
from sort import *

class SyntaxParser():

    lexical = None
    lookahead = None
    
    def __init__(self, sentence):
        self.lexical = LexicalParser(sentence)

    def get_lookahead(self):
        return self.lookahead

    def shift(self):
        self.lookahead = self.lexical.get_lexeme()
        print("lookahead: "+str(self.lookahead))

    def parse_error(self):
        print("Parsing error")

    def parse(self):
        raise NotImplementedError

class SQLSyntaxParser(SyntaxParser):

    def __init__(self, sentence):
        self.lexical = SQLLexicalParser(sentence)
    
    def parse(self):
        self.shift()
        return self.query_list()

    def query_list(self):
        if(self.get_lookahead() == self.lexical._opening):
            self.shift()
            tree = AbstractTree(self.lexical._query)
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
            tree = AbstractTree(self.lexical._query)
            tree_query = self.query()
            tree.concatenate_father_son(tree_query)
            tree_list = self.query_list_next()
            tree.concatenate_father_brother(tree_list)
            return tree

    def query_list_next(self):
        if(self.get_lookahead() == self.lexical._name):
            tree = AbstractTree(self.lexical.get_text())
            self.shift()
            tree_list = self.query_list()
            tree.concatenate_father_brother(tree_list)
            return tree

    def query(self):
        if(self.get_lookahead() == self.lexical._select):
            self.shift()
            tree = AbstractTree(self.lexical._select)
            tree_mode = self.select_mode()
            tree_select = self.select()
            if(tree_mode == None):
                tree.concatenate_father_son(tree_select)
            else:
                tree.concatenate_father_son(tree_mode)
                tree_mode.concatenate_father_son(tree_select)
            if(self.get_lookahead() == self.lexical._from):
                self.shift()
                tree_from = AbstractTree(self.lexical._from)
                tree_name = self.column_list()
                tree_next = self.query_next()
                tree_from.concatenate_father_son(tree_name)
                tree_from.concatenate_father_brother(tree_next)
                tree.concatenate_father_brother(tree_from)
                return tree
            else:
                self.parse_error()
        else:
            self.parse_error()

    def select_mode(self):
        if(self.get_lookahead() == self.lexical._distinct):
            self.shift()
            tree_disctinct = AbstractTree(self.lexical._stardistinct)
            return tree_disctinct

    def select(self):
        if(self.get_lookahead() == self.lexical._star):
            self.shift()
            tree_star = AbstractTree(self.lexical._star)
            return tree_star
        else:
            tree = self.column_select_list()
            return tree

    def column(self):
        if(self.get_lookahead() == self.lexical._name):
            tree = AbstractTree(self.lexical.get_text())
            self.shift()
            tree_next = self.column_next()
            tree.concatenate_father_son(tree_next)
            return tree
        else:
            self.parse_error()

    def column_next(self):
        if(self.get_lookahead() == self.lexical._dot):
            self.shift()
            if(self.get_lookahead() == self.lexical._name):
                tree_dot = AbstractTree(self.lexical._dot)
                tree_dot.concatenate_father_son(AbstractTree(self.lexical.get_text()))
                self.shift()
                return tree_dot
            else:
                self.parse_error()
        elif(self.get_lookahead() == self.lexical._opening):
            self.shift()
            tree = self.column()
            if(self.get_lookahead() == self.lexical._closing):
                self.shift()
                return tree
            else:
                self.parse_error()

    def column_select_list(self):
        tree_column = self.column()
        tree_as = self.column_as()
        tree_select = self.column_select_list_next()
        tree_column.concatenate_father_son(tree_as)
        tree_column.concatenate_father_brother(tree_select)
        return tree_column

    def column_as(self):
        if(self.get_lookahead() == self.lexical._as):
            self.shift()
            if(self.get_lookahead() == self.lexical._name):
                tree_as = AbstractTree(self.lexical._as)
                tree_as.concatenate_father_son(AbstractTree(self.lexical.get_text()))
                self.shift()
                return tree_as
            else:
                self.parse_error()

    def column_select_list_next(self):
        if(self.get_lookahead() == self.lexical._comma):
            self.shift()
            tree = self.column_select_list()
            return tree

    def column_list(self):
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
            tree = AbstractTree(self.lexical.get_text())
            self.shift()
            tree_list = self.name_list_next()
            tree.concatenate_father_brother(tree_list)
            return tree
        else:
            self.parse_error()

    def name_list_next(self):
        if(self.get_lookahead() == self.lexical._comma):
            self.shift()
            tree = self.name_list()
            return tree

    def query_next(self):
        if(self.get_lookahead() == self.lexical._where):
            self.shift()
            tree_condition = self.condition()
            tree_group_by = self.group_by()
            tree_where = AbstractTree(self.lexical._where)
            tree_where.concatenate_father_son(tree_condition)
            tree_where.concatenate_father_brother(tree_group_by)
            return tree_where
        else:
            tree = self.group_by()
            return tree

    def group_by(self):
        if(self.get_lookahead() == self.lexical._group_by):
            self.shift()
            tree_column = self.column_list()
            tree_having = self.having()
            tree_group_by = AbstractTree(self.lexical._group_by)
            tree_group_by.concatenate_father_son(tree_column)
            tree_group_by.concatenate_father_brother(tree_having)
        else:
            tree = self.having()
            return tree

    def having(self):
        if(self.get_lookahead() == self.lexical._having):
            self.shift()
            tree_condition = self.condition()
            tree_order = self.order()
            tree_having = AbstractTree(self.lexical._having)
            tree_having.concatenate_father_son(tree_condition)
            tree_having.concatenate_father_brother(tree_order)
            return tree_having
        else:
            tree = self.order()
            return tree

    def order(self):
        if(self.get_lookahead() == self.lexical._order_by):
            self.shift()
            tree_column = self.column_list()
            tree_order_op = self.order_op()
            tree_order_by = AbstractTree(self.lexical._order_by)
            tree_order_by.concatenate_father_son(tree_column)
            return tree_order_by

    def order_op(self):
        if(self.get_lookahead() == self.lexical._asc):
            self.shift()
            return AbstractTree(self.lexical._asc)
        elif(self.get_lookahead() == self.lexical._desc):
            self.shift()
            return AbstractTree(self.lexical._desc)
        else:
            self.parse_error()

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
            self.shift()
            tree = self.condition()
            tree_and = AbstractTree(self.lexical._and)
            tree_and.concatenate_father_son(tree)
            return tree_and
        elif(self.get_lookahead() == self.lexical._or):
            self.shift()
            tree = self.condition()
            tree_or = AbstractTree(self.lexical._or)
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
                self.parse_error()
        elif(self.get_lookahead() == self.lexical._not):
            self.shift()
            tree = self.test_other()
            tree_not = AbstractTree(self.lexical._not)
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
            self.shift()
            if(self.get_lookahead() == self.lexical._exp):
                tree_like = AbstractTree(self.lexical._like)
                tree_like.concatenate_father_son(AbstractTree(self.lexical.get_text()))
                self.shift()
                return tree_like
            else:
                self.parse_error()
        elif(self.get_lookahead() == self.lexical._in):
            self.shift()
            if(self.get_lookahead() == self.lexical._opening):
                self.shift()
                tree = self.query_list()
                if(self.get_lookahead() == self.lexical._closing):
                    self.shift()
                    tree_in = AbstractTree(self.lexical._in)
                    tree_in.concatenate_father_son(tree)
                    return tree_in
                else:
                    self.parse_error()
            else:
                self.parse_error()
        else:
            self.parse_error()

    def test_next(self):
        if(self.get_lookahead() == self.lexical._opening):
            self.shift()
            tree = self.query_list()
            if(self.get_lookahead() == self.lexical._closing):
                self.shift()
            else:
                self.parse_error()
        elif(self.get_lookahead() == self.lexical._quote or self.get_lookahead() == self.lexical._double_quote or self.get_lookahead() == self.lexical._number):
            tree = self.value()
        else:
            tree = self.column()
        return tree

    def op(self):
        if(self.get_lookahead() == self.lexical._equal):
            self.shift()
            return AbstractTree(self.lexical._equal)
        elif(self.get_lookahead() == self.lexical._not_equal):
            self.shift()
            return AbstractTree(self.lexical._not_equal)
        elif(self.get_lookahead() == self.lexical._less):
            self.shift()
            return AbstractTree(self.lexical._less)
        elif(self.get_lookahead() == self.lexical._greater):
            self.shift()
            return AbstractTree(self.lexical._greater)
        elif(self.get_lookahead() == self.lexical._less_e):
            self.shift()
            return AbstractTree(self.lexical._less_e)
        elif(self.get_lookahead() == self.lexical._greater_e):
            self.shift()
            return AbstractTree(self.lexical._greater_e)
        else:
            self.parse_error()

    def value(self):
        if(self.get_lookahead() == self.lexical._quote):
            self.shift()
            if(self.get_lookahead() == self.lexical._name):
                tree = AbstractTree(get_text())
                self.shift()
                if(self.get_lookahead() == self.lexical._quote):
                    self.shift()
                    return tree
                else:
                    self.parse_error()
            else:
                self.parse_error()
        elif(self.get_lookahead() == self.lexical._double_quote):
            self.shift()
            if(self.get_lookahead() == self.lexical._name):
                tree = AbstractTree(get_text())
                self.shift()
                if(self.get_lookahead() == self.lexical._double_quote):
                    self.shift()
                    return tree
                else:
                    self.parse_error()
            else:
                self.parse_error()
        elif(self.get_lookahead() == self.lexical._number):
            tree = AbstractTree(self.lexical.get_text())
            self.shift()
            return tree
        else:
            self.parse_error()

            
p = SQLSyntaxParser("SELECT * FROM t1.b,t1.a,t1.b  WHERE t1 = t2.coucou AND qui.qui = truc OR machin = bidule")
tree = p.parse()
print(tree)
