function get_length() {
  /* Get the position of the cursor */
  var e = document.getElementById("input_text");
  var length = 0;
  var i=0;
  /* If the cursor was not in the node  */
  while(i<e.childNodes.length &&  e.childNodes.item(i).childNodes.item(0) != null && e.childNodes.item(i).childNodes.item(0) != window.getSelection().focusNode) {
    /* We increment the length */
    length += e.childNodes.item(i).childNodes.item(0).nodeValue.length;
	  i++;
  }
  /* If we are in the node, we add the offset */
  length += window.getSelection().getRangeAt(0).startOffset;
  return length;
}

function set_cursor(length) {
  /* Place the cursor at the same position as it was before */
  var e = document.getElementById("input_text");
  for(var i=0; i<e.childNodes.length; i++) {
    /* We take the text inside the colored node */
	  var n_e = e.childNodes.item(i).childNodes.item(0);
	  if(n_e != null) {
	    var n = n_e.nodeValue;
	    var n_length = n.length;
	    if(n_length >= length) {
        /* The cursor was in this node ! We place the cursor ! */
		    var range = document.createRange();
		    range.setStart(n_e,length);
	  	  window.getSelection().removeAllRanges();
		    window.getSelection().addRange(range);
		    return;
	    } else {
        /* If the cursor was not in this node ... */
		    length -= n_length;
	    }
	  } 
  }    
}

function delete_br() {
  /* Delete <br/> which are added by the web browser and the user. 
  Actualy, Firefox add a <br> when the div is empty */
  var e = document.getElementById("input_text");
  var l = e.getElementsByTagName("br");
  for(var i=0; i<l.length; i++) {
	  l.item(i).remove();
  }
}

function set_space() {
  /* Set the normal space as a non-breakable space */
  var e = document.getElementById("input_text");
  for(var i=0; i<e.childNodes.length; i++) {
    var n_e = e.childNodes.item(i);
	  if(n_e.innerHTML != undefined) {
	    n_e.innerHTML = n_e.innerHTML.replace(" ", "&nbsp;");
	  }
  }
}

function color() {
  input_text = document.getElementById("input_text");
  /* We take the position of the cursor */
  l = get_length();

  /* We delete the <br/> */
  delete_br();
  /* We set the right space */
  set_space();
  
  /* We take the sentence */
  var sentence = input_text.innerText;
    
  /* We parse the sentence */
  var p = new SQLSyntaxParser(sentence);
	try{
	    p.parse();
	}catch(e){}
  
  /* We color the editor ! :) */
	var tabcolor = p.highlighting;
	console.log(tabcolor);
	input_text.innerHTML = "";
	console.log(tabcolor);
	for(var i=0; i< tabcolor.length; i++){
	    var span = document.createElement("span");
	    span.innerText = tabcolor[i][0];
	    span.style.color = tabcolor[i][1];
	    input_text.appendChild(span);
	}
  /* And we set the cursor at the right place */
  set_cursor(l);

  predict(p.predict);
}

function predict(predict_set) {
  input_predict = document.getElementById("input_predict");
  input_predict.innerHTML = "";
  var ul = document.createElement("ul");
  for(var i=0; i<predict_set.length; i++) {
    var li = document.createElement("li");
    ul.appendChild(li);
    p = new SQLLexicalParser("");
    
    switch(predict_set[i]) {
      case p._query:
        li.innerText = "Requete";
        break;
      case p._opening:
        li.innerText = "(";
        break;
      case p._closing:
        li.innerText = ")";
        break;
      case p._star:
        li.innerText = "*";
        break;
      case p._dot:
        li.innerText = ".";
        break;
      case p._comma:
        li.innerText = ",";
        break;
      case p._quote:
        li.innerText = "\'";
        break;
      case p._double_quote:
        li.innerText = "\"";
        break;
      
      case p._equal:
        li.innerText = "=";
        break;
      case p._not_equal:
        li.innerText = "!=";
        break;
      case p._less_e:
        li.innerText = "<=";
        break;
      case p._greater_e:
        li.innerText = ">=";
        break;
      case p._less:
        li.innerText = "<";
        break;
      case p._greater:
        li.innerText = ">";
        break;

      case p._select_distinct:
        li.innerText = "SELECT DISTINCT";
        break;
      case p._select:
        li.innerText = "SELECT";
        break;
      case p._from:
        li.innerText = "FROM";
        break;
      case p._as:
        li.innerText = "AS";
        break;
      case p._where: 
        li.innerText = "WHERE";
        break;
      case p._group_by:
        li.innerText = "GROUP BY";
        break;
      case p._having:
        li.innerText = "HAVING";
        break;
      case p._order_by:
        li.innerText = "ORDER BY";
        break;
      case p._asc:
        li.innerText = "ASC";
        break;
      case p._desc:
        li.innerText = "DESC";
        break;
      case p._and:
        li.innerText = "AND";
        break;
      case p._or:
        li.innerText = "OR";
        break;
      case p._not:
        li.innerText = "NOT";
        break;
      case p._like:
        li.innerText = "LIKE";
        break;
      case p._in:
        li.innerText = "IN";
        break;
      case p._name:
        li.innerText = "Texte";
        break;
      case p._number:
        li.innerText = "Nombre";
        break;
      default:
        li.innerText = "Autre";
    }
  }
  input_predict.appendChild(ul);
}
