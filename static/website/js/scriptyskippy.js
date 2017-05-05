function get_token(){
    var cookies=document.cookie.split(";");
    var token;
    for (var i = 0 ; i < cookies.length ; i++) {
	cookies[i]=cookies[i].split('=');
	if (cookies [i][0] === "csrftoken" )
	    token = cookies [i][1];
    }
    return(token);
}

function get_request() {    
    var input = $("#input_text").text().replace(/\s/g, " ");
    $.ajax({
	url : '/request/', 
	type : 'POST' ,
	headers: {
            'X-CSRFToken': get_token()
	},
	data : { query : input, exercise_no : $("#exercise_selection").val(), question_no : $("#question_selection").val() },	
	success : function(data, status){
	    if (status ==="success")
		$("#output_request").html( data );
	}
    });
}

function get_expected_request() {
    $.ajax({
	url : '/expected_request/', 
	type : 'POST' ,
	headers: {
            'X-CSRFToken': get_token()
	},
	data : {exercise_no : $("#exercise_selection").val(), question_no : $("#question_selection").val() },	
	success : function(data, status){
	    if (status ==="success")
		$("#expected_request").html( data );
	}
    });   
}

function reset_tables() {
    $.ajax({
	url : '/reset/', 
	type : 'POST' ,
	headers: {
            'X-CSRFToken': get_token()
	},
	data : { exercise_no : $("#exercise_selection").val() }
    });   
}

function get_label() {
    $.ajax({
	url : '/label/', 
	type : 'POST' ,
	headers: {
            'X-CSRFToken': get_token()
	},
	data : { exercise_no : $("#exercise_selection").val(), question_no : $("#question_selection").val() },	
	success : function(data, status){
	    if (status ==="success")
		$("#question_label").html( data );
	}
    });   
}

function get_question() {    
    $.ajax({
	url : '/question/', 
	type : 'POST' ,
	headers: {
            'X-CSRFToken': get_token()
	},
	data : { exercise_no : $("#exercise_selection").val() },	
	success : function(data, status){
	    if (status ==="success")
		$("#question").html( data );
	}
    });   
}

function get_hint() {
    var input = $("#input_text").text().replace(/\s/g, " ");
    $.ajax({
	url : '/hint/', 
	type : 'POST' ,
	headers: {
            'X-CSRFToken': get_token()
	},
	data : { exercise_no : $("#exercise_selection").val(), question_no : $("#question_selection").val(), query : input },	
	success : function(data, status){
	    if (status ==="success")
		$("#hint").html(data);
	}
    });   
}

function get_tables() {    
    $.ajax({
	url : '/tables/', 
	type : 'POST' ,
	headers: {
            'X-CSRFToken': get_token()
	},
	data : { exercise_no : $("#exercise_selection").val()},	
	success : function(data, status){
	    if (status ==="success")
		$("#tables").html(data);
	}
    });   
}

function get_length() {
    var e = document.getElementById("input_text");
    var length = 0;
    var i=0;
    while(i<e.childNodes.length &&  e.childNodes.item(i).childNodes.item(0) != null && e.childNodes.item(i).childNodes.item(0) != window.getSelection().focusNode) {
	length += e.childNodes.item(i).childNodes.item(0).nodeValue.length;
	i++;
    }

    length += window.getSelection().getRangeAt(0).startOffset;
    return length;
}

function set_cursor(length) {
    var e = document.getElementById("input_text");
    for(var i=0; i<e.childNodes.length; i++) {
	var n_e = e.childNodes.item(i).childNodes.item(0);
	if(n_e != null) {
	    var n = n_e.nodeValue;
	    var n_length = n.length;
	    if(n_length >= length) {
		var range = document.createRange();
		range.setStart(n_e,length);
		window.getSelection().removeAllRanges();
		window.getSelection().addRange(range);
		return;
	    }
	    else {
		length -= n_length;
	    }
	}
    }    
}

function delete_br() {
    var e = document.getElementById("input_text");
    var l = e.getElementsByTagName("br");
    for(var i=0; i<l.length; i++) {
	l.item(i).remove();
    }
}

function set_space() {
    var e = document.getElementById("input_text");
    for(var i=0; i<e.childNodes.length; i++) {
	var n_e = e.childNodes.item(i);
	if(n_e.innerHTML != undefined) {
	    n_e.innerHTML = n_e.innerHTML.replace(" ", "&nbsp;");
	}
    }
}

function color(){
    input_text = document.getElementById("input_text");
    l = get_length();

    delete_br();
    set_space();
    
    var sentence = input_text.innerText;
    var last_letter = sentence[sentence.length-1];
    
    var p = new SQLSyntaxParser(sentence);
	
	try{
	    p.parse();
	}catch(e){}
    
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

    console.log("len: "+l);
    set_cursor(l);
}
