function get_token() {
  /* Get the token in the cookie (see the Django documentation) */
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
	  success : function(data, status) {
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
	  success : function(data, status) {
	    if (status ==="success")
		    $("#question").html( data );
        get_expected_request();
        get_label();
        get_tables();
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
	  success : function(data, status) {
	    if (status ==="success")
		    $("#tables").html(data);
	  }
  });   
}
