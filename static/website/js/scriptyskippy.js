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
function post_ajax() {    
    get_token();
    $.ajax({
	url : '/request/', 
	type : 'POST' ,
	headers: {
            'X-CSRFToken': get_token()
	},
	success : function(data, status){
	    if (status ==="success")
		$("#output_request").html( data );
	}
    });

    
    
}
