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
  var table = document.createElement("table");
  var tr = document.createElement("tr");
   table.appendChild(tr);

  for(var i=0; i<predict_set.length; i++) {
    var td = document.createElement("td");
    tr.appendChild(td);
    p = new SQLLexicalParser("");
    
    switch(predict_set[i]) {
      case p._query:
        td.innerText = "Requete";
        break;
      case p._opening:
        td.innerText = "(";
        break;
      case p._closing:
        td.innerText = ")";
        break;
      case p._star:
        td.innerText = "*";
        break;
      case p._dot:
        td.innerText = ".";
        break;
      case p._comma:
        td.innerText = ",";
        break;
      case p._quote:
        td.innerText = "\'";
        break;
      case p._double_quote:
        td.innerText = "\"";
        break;
      
      case p._equal:
        td.innerText = "=";
        break;
      case p._not_equal:
        td.innerText = "!=";
        break;
      case p._less_e:
        td.innerText = "<=";
        break;
      case p._greater_e:
        td.innerText = ">=";
        break;
      case p._less:
        td.innerText = "<";
        break;
      case p._greater:
        td.innerText = ">";
        break;

      case p._select_distinct:
        td.innerText = "SELECT DISTINCT";
        break;
      case p._select:
        td.innerText = "SELECT";
        break;
      case p._from:
        td.innerText = "FROM";
        break;
      case p._as:
        td.innerText = "AS";
        break;
      case p._where: 
        td.innerText = "WHERE";
        break;
      case p._group_by:
        td.innerText = "GROUP BY";
        break;
      case p._having:
        td.innerText = "HAVING";
        break;
      case p._order_by:
        td.innerText = "ORDER BY";
        break;
      case p._asc:
        td.innerText = "ASC";
        break;
      case p._desc:
        td.innerText = "DESC";
        break;
      case p._and:
        td.innerText = "AND";
        break;
      case p._or:
        td.innerText = "OR";
        break;
      case p._not:
        td.innerText = "NOT";
        break;
      case p._like:
        td.innerText = "LIKE";
        break;
      case p._in:
        td.innerText = "IN";
        break;
      case p._name:
        td.innerText = "Texte";
        break;
      case p._number:
        td.innerText = "Nombre";
        break;
      default:
        li.innerText = "Autre";
    }
  }
  input_predict.appendChild(table);
}
