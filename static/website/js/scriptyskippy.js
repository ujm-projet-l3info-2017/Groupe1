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
    $("#output_request").html( "Next Step..." );   
    get_token();
    $.ajax({
	url : '/request/', 
	type : 'POST' ,
	headers: {
            'X_CSRF_TOKEN': get_token()
	},
    });
    
}
