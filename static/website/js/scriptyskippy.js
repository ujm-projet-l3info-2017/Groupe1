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
    $.ajax({
	url : '/request/', 
	type : 'POST' ,
	headers: {
            'X-CSRFToken': get_token()
	},
	data : { query : $("#input textarea").val(), exercise_no : $("#exercise_selection").val(), question_no : $("#question_selection").val() },	
	success : function(data, status){
	    if (status ==="success")
		$("#output_request").html( data );
	}
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
