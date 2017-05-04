function LexicalParser(sentence) {
    this.sentence = sentence;
    this.length = 0;
    this.text = "";

    this.match = function(regex) {
	var m = this.sentence.match(new RegExp('^'+regex));
	if(m == null) {
	    return null;
	} else {
	    m = m[0];
	}
	this.length = m.length;
	this.text = m;
	this.shift(this.length);
	return this.text;
    }

    this.shift = function(length) {
	this.sentence = this.sentence.substring(length);
    }

    this.get_text = function() {
	return this.text.toLowerCase();
    }
}

function SQLLexicalParser(sentence) {
    LexicalParser.call(this, sentence);

    this._query = 0;
    this._opening = 1;
    this._closing = 2;
    this._star = 3;
    this._dot = 4;
    this._comma = 5;
    this._quote = 6;
    this._double_quote = 7;

    this._equal = 8;
    this._not_equal = 9;
    this._less_e = 10;
    this._greater_e = 11;
    this._less = 12;
    this._greater = 13;

    this._select_distinct = 14;
    this._select = 15;
    this._from = 16;
    this._as = 17;
    this._where = 18;
    this._group_by = 19;
    this._having = 20;
    this._order_by = 21;
    this._asc = 22;
    this._desc = 23;
    this._and = 24;
    this._or = 25;
    this._not = 26;
    this._like = 27;
    this._in = 28;
    this._name = 29;
    this._number = 30;

    this.color = ["", "red", "red", "blue", "black", "black", "blue", "blue",
		  "black", "black", "black", "black", "black", "black",
		  "green", "green", "green", "green", "green", "green", "green", "green", "green", "green", "green", "green", "green", "green", "green", "blue", "blue"];
    
    this.get_lexeme = function() {
	if (this.match("\\(")) { return this._opening; }
	if (this.match("\\)")) { return this._closing; }
        if (this.match("\\*")) { return this._star; }
        if (this.match("\\.")) { return this._dot; }
        if (this.match(",")) { return this._comma; }
        if (this.match("'")) { return this._quote; }
        if (this.match('\\"')) { return this._double_quote; }

        if (this.match("=")) { return this._equal; }
        if (this.match("<>|!=")) { return this._not_equal; }
        if (this.match("<=")) { return this._less_e; }
        if (this.match(">=")) { return this._greater_e; }
        if (this.match("<")) { return this._less; }
        if (this.match(">")) { return this._greater; }

        if (this.match("(SELECT|select)[ ]+(DISTINCT|distinct)")) { return this._select_distinct; }
        if (this.match("SELECT|select")) { return this._select; }
        if (this.match("FROM|from")) { return this._from; }
        if (this.match("AS|as")) { return this._as; }
        if (this.match("WHERE|where")) { return this._where; }
        if (this.match("(GROUP|group)[ ]+(BY|by)")) { return this._group_by; }
        if (this.match("HAVING|having")) { return this._having; }
        if (this.match("ORDER[ ]+BY")) { return this._order_by; }
        if (this.match("ASC|asc")) { return this._asc; }
        if (this.match("DESC|desc")) { return this._desc; }
        if (this.match("AND|and")) { return this._and; }
        if (this.match("OR|or")) { return this._or; }
        if (this.match("NOT|not")) { return this._not; }
        if (this.match("LIKE|like")) { return this._like; }
        if (this.match("IN|in")) { return this._in; }

        if (this.match("[a-zA-Z0-9]+")) { return this._name; }
        if (this.match("[0-9]+")) { return this._number; }
        if (this.match("[ ]+")) { return this.get_lexeme(); }
	return -1;
    }
}
