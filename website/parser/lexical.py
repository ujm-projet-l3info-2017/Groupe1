import re

class LexicalParser():

    sentence = ""
    length = 0
    text = ""
    
    def __init__(self, sentence):
        self.sentence = sentence
        
    def match(self, regex):
        m = re.match(r"^"+regex, self.sentence)
        if(m == None):
            return None
        self.length = len(m.group(0))
        self.text = m.group(0)
        self.shift(self.length)
        return m.group(0)

    def shift(self, length):
        self.sentence = self.sentence[self.length:]

    def get_text(self):
        return self.text
    
    def get_lexeme(self):
        raise NotImplementedError

class SQLLexicalParser(LexicalParser):

    _query = 0
    _opening = 1
    _closing = 2
    _star = 3
    _dot = 4
    _comma = 5
    _quote = 6
    _double_quote = 7

    _equal = 8
    _not_equal = 9
    _less_e = 10
    _greater_e = 11
    _less = 12
    _greater = 13

    _select = 14
    _from = 15
    _distinct = 16
    _as = 17
    _where = 18
    _group_by = 19
    _having = 20
    _order_by = 21
    _asc = 22
    _desc = 23
    _and = 24
    _or = 25
    _not = 26
    _like = 27
    _in = 28
    _name = 29
    _number = 30
    
    def get_lexeme(self):
        if self.match("\(") : return self._opening
        if self.match("\)") : return self._closing
        if self.match("\*") : return self._star
        if self.match("\.") : return self._dot
        if self.match(",") : return self._comma
        if self.match("'") : return self._quote
        if self.match("\"") : return self._double_quote

        if self.match("=") : return self._equal
        if self.match("<>|!=") : return self._not_equal
        if self.match("<=") : return self._less_e
        if self.match(">=") : return self._greater_e
        if self.match("<") : return self._less
        if self.match(">") : return self._greater

        if self.match("SELECT|select") : return self._select
        if self.match("FROM|from") : return self._from
        if self.match("DISTINCT|distinct") : return self._distinct
        if self.match("AS|as") : return self._as
        if self.match("WHERE|where") : return self._where
        if self.match("(GROUP|group)[ ]+(BY|by)") : return self._group_by
        if self.match("HAVING|having") : return self._having
        if self.match("ORDER[ ]+BY") : return self._order_by
        if self.match("ASC|asc") : return self._asc
        if self.match("DESC|desc") : return self._desc
        if self.match("AND|and") : return self._and
        if self.match("OR|or") : return self._or
        if self.match("NOT|not") : return self._not
        if self.match("LIKE|like") : return self._like
        if self.match("IN|in") : return self._in

        if self.match("[a-zA-Z0-9]+") : return self._name
        if self.match("[0-9]+") : return self._number
        if self.match("[ ]+") : return self.get_lexeme()