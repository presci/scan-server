var a = (function(){
	var init=function(){
	    $('#login').click(function(){
		    var myuri="https://accounts.google.com/o/oauth2/auth?scope="+encodeURIComponent('')+ "&redirect_uri="+encodeURIComponent('http://localhost:9093/token')+"&response_type=code&client_id=";

		    window.open(myuri,"_blank","menubar=no,toolbar=no, scrollbars=no, resizable=no, top=500, left=500, width=400, height=400");
		});
	}

	init();
    })();  
