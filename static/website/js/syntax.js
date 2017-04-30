function SyntaxParser(sentence) {
    this.lexical = new LexicalParser(sentence);
    this.lookahead = null;

    this.shift = function() {
	this.lookahead = this.lexical.get_lexeme();
    }

    this.parse_error = function() {}
    this.parse = function() {}
}

function SQLSyntaxParser(sentence) {
    SyntaxParser.call(this, sentence);

    this.lexical = new SQLLexicalParser(sentence);
    this.highlighting = [];
    
    this.color = function() {
	this.highlighting.push([this.lexical.text, this.lexical.color[this.lookahead]]);
    }

    this.parse_error = function() {
	while(this.lookahead != -1) {
	    this.highlighting.push([this.lexical.text, "black"]);
	    this.shift();
	}
	throw new Error("Parse error");
    }
    
    this.parse = function() {
	this.shift();
	this.query_list();
    }

    this.query_list = function() {
	if(this.lookahead == this.lexical._opening) {
	    this.color();
	    this.shift();
	    this.query();
	    if(this.lookahead == this.lexical._closing) {
		this.color();
		this.shift();
		this.query_list_next();
	    }
	    else {
		return this.parse_error();
	    }
	} else {
	    this.query();
	    this.query_list_next();
	}
    }

    this.query_list_next = function() {
	if(this.lookahead == this.lexical._name) {
	    this.color();
	    this.shift();
	    this.query_list();
	}
    }

    this.query = function() {
	this.select_mode();
	this.select();
	if(this.lookahead == this.lexical._from) {
	    this.color();
	    this.shift();
	    this.query_next();
	} else {
	    this.parse_error();
	}
    }

    this.select_mode = function() {
	if(this.lookahead == this.lexical._select_distinct) {
	    this.color();
	    this.shift();
	} else if(this.lookahead == this.lexical._select) {
	    this.color();
	    this.shift();
	} else {
	    this.parse_error();
	}
    }

    this.select = function() {
	if(this.lookahead == this.lexical._star) {
	    this.color();
	    this.shift();
	} else {
	    this.column_select_list();
	}
    }

    this.column = function() {
	if(this.lookahead == this.lexical._name) {
	    this.color();
	    this.shift();

	    this.column_next();
	} else {
	    this.parse_error();
	}
    }

    this.column_next = function() {
	if(this.lookahead == this.lexical._dot) {
	    this.color();
	    this.shift();

	    if(this.lookahead == this.lexical._name) {
		this.color();
		this.shift();
	    } else {
		this.parse_error();
	    }
	} else if(this.lookahead == this.lexical._opening) {
	    this.color();
	    this.shift();
	    this.column();
	    if(this.lookahead == this.lexical._closing) {
		this.color();
		this.shift();
	    } else {
		this.parse_error();
	    }
	}
    }

    this.column_select_list = function() {
	this.column();
	this.column_as();
	this.column_select_list_next();
    }

    this.column_as = function() {
	if(this.lookahead == this.lexical._as) {
	    this.color();
	    this.shift();

	    if(this.lookahead == this.lexical._name) {
		this.color();
		this.shift();
	    } else {
		this.parse_error();
	    }
	}
    }

    this.column_select_list_next = function() {
	if(this.lookahead == this.lexical._comma) {
	    this.color();
	    this.shift();
	    this.column_select_list();
	}
    }

    this.column_list = function() {
	this.column();
	this.column_list_next();
    }

    this.column_list_next = function() {
	if(this.lookahead == this.lexical._comma) {
	    this.color();
	    this.shift();
	    this.column_list();
	}
    }

    this.name_list = function() {
	if(this.lookahead == this.lexical._name) {
	    this.color();
	    this.shift();
	    this.name_list_next();
	} else {
	    this.parse_error();
	}
    }

    this.name_list_next = function() {
	if(this.lookahead == this.lexical._comma) {
	    this.color();
	    this.shift();
	    this.name_list();
	}
    }

    this.query_next = function() {
	if(this.lookahead == this.lexical._where) {
	    this.color();
	    this.shift();
	    this.condition();
	    this.group_by();
	} else {
	    this.group_by();
	}
    }

    this.group_by = function() {
	if(this.lookahead == this.lexical._group_by) {
	    this.color();
	    this.shift();
	    this.column_list();
	    this.having();
	} else {
	    this.having();
	}
    }

    this.having = function() {
	if(this.lookahead == this.lexical._having) {
	    this.color();
	    this.shift();
	    this.condition();
	    this.order();
	} else {
	    this.order();
	}
    }

    this.order = function() {
	if(this.lookahead == this.lexical._order_by) {
	    this.color();
	    this.shift();
	    this.column_list();
	    this.order_op();
	}
    }

    this.order_op = function() {
	if(this.lookahead == this.lexical.asc) {
	    this.color();
	    this.shift();
	} else if(this.lookahead == this.lexical.desc) {
	    this.color();
	    this.shift();
	} else {
	    this.parse_error();
	}
    }

    this.condition = function() {
	this.test();
	this.condition_next();
    }

    this.condition_next = function() {
	if(this.lookahead == this.lexical._and) {
	    this.color();
	    this.shift();
	    this.condition();
	} else if(this.lookahead == this.lexical._or) {
	    this.color();
	    this.shift();
	    this.condition();
	}
    }

    this.test = function() {
	if(this.lookahead == this.lexical._opening) {
	    this.color();
	    this.shift();
	    this.condition();
	    if(this.lookahead == this.lexical._closing) {
		this.color();
		this.shift();
	    } else {
		this.parse_error();
	    }
	} else if(this.lookahead == this.lexical._not) {
	    this.color();
	    this.shift();
	    this.test_other();
	} else if(this.lookahead == this.lexical._like || this.lookahead == this.lexical._in) {
	    this.test_other();
	} else {
	    this.column();
	    this.op();
	    this.test_next();
	}
    }

    this.test_other = function() {
	if(this.lookahead == this.lexical._like) {
	    this.color();
	    this.shift();
	    if(this.lookahead == this.lexical._exp) {
		this.color();
		this.shift();
	    } else {
		this.parse_error();
	    }
	} else if(this.lookahead == this.lexical._in) {
	    this.color();
	    this.shift();
	    if(this.lookahead == this.lexical._opening) {
		this.color();
		this.shift();
		this.query_list();
		if(this.lookahead == this.lexical._closing) {
		    this.color();
		    this.shift();
		} else {
		    this.parse_error();
		}
	    } else {
		this.parse_error();
	    }
	} else {
	    this.parse_error();
	}
    }

    this.test_next = function() {
	if(this.lookahead == this.lexical._opening) {
	    this.color();
	    this.shift();
	    this.query_list();
	    if(this.lookahead == this.lexical._closing) {
		this.color();
		this.shift();
	    } else {
		this.parse_error();
	    }
	} else if(this.lookahead == this.lexical._quote || this.lookahead == this.lexical._double_quote || this.lookahead == this.lexical._number) {
	    this.value();
	} else {
	    this.column();
	}
    }

    this.op = function() {
	if(this.lookahead == this.lexical._equal) {
	    this.color();
	    this.shift();
	} else if(this.lookahead == this.lexical._not_equal) {
	    this.color();
	    this.shift();
	} else if(this.lookahead == this.lexical._less) {
	    this.color();
	    this.shift();
	} else if(this.lookahead == this.lexical._greater) {
	    this.color();
	    this.shift();
	} else if(this.lookahead == this.lexical._less_e) {
	    this.color();
	    this.shift();
	} else if(this.lookahead == this.lexical._greater_e) {
	    this.color();
	    this.shift();
	} else {
	    this.parse_error();
	}
    }

    this.value = function() {
	if(this.lookahead == this.lexical._quote) {
	    this.color();
	    this.shift();
	    if(this.lookahead == this.lexical._name) {
		this.color();
		this.shift();
		if(this.lookahead == this.lexical._quote) {
		    this.color();
		    this.shift();
		} else {
		    this.parse_error();
		}
	    } else {
		this.parse_error();
	    }
	} else if(this.lookahead == this.lexical._double_quote) {
	    this.color();
	    this.shift();
	    if(this.lookahead == this.lexical._name) {
		this.color();
		this.shift();
		if(this.lookahead == this.lexical._double_quote) {
		    this.color();
		    this.shift();
		} else {
		    this.parse_error();
		}
	    } else {
		this.parse_error();
	    }
	} else if(this.lookahead == this.lexical._number) {
	    this.color();
	    this.shift();
	} else {
	    this.parse_error();
	}
    }
}
