var a = (function(){
	var init=function(){
	    $('#login').click(function(){
		    var myuri="https://accounts.google.com/o/oauth2/auth?scope="+encodeURIComponent('https://www.googleapis.com/auth/drive https://www.googleapis.com/auth/drive.appdata https://www.googleapis.com/auth/drive.file')+ "&redirect_uri="+encodeURIComponent('http://localhost:9093/token')+"&response_type=code&client_id=284508695390-gotsg7835gar48pr41g3o5qi5i0f92t5.apps.googleusercontent.com";

		    window.open(myuri,"_blank","menubar=no,toolbar=no, scrollbars=no, resizable=no, top=500, left=500, width=400, height=400");
		});
	}

	init();
    })();  
