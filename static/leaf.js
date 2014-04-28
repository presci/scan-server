String.prototype.endswith = function(suffix) {
    return this.indexOf(suffix, this.length - suffix.length) !== -1;
};

var a = (function(){
	var init=function(){
	    $('#login').click(function(){
		    var myuri="https://accounts.google.com/o/oauth2/auth?scope="+encodeURIComponent('https://www.googleapis.com/auth/drive https://www.googleapis.com/auth/drive.appdata https://www.googleapis.com/auth/drive.file')+ "&redirect_uri="+encodeURIComponent('http://localhost:9093/token')+"&response_type=code&client_id=284508695390-gotsg7835gar48pr41g3o5qi5i0f92t5.apps.googleusercontent.com";
		    window.location.assign(myuri);
		});
	    $('#startscan').click(function(){
		    $.ajax({
			    url:'http://localhost:9093/scan',
				beforeSend:function(xhr){
				xhr.overrideMimeType('text/plain; charset=x-user-defined');
			    }}).done(function(data, textstatus, jq){
				    console.log(jq);
				});
		});
	    $('#stopscan').click(function(){
		    $.ajax({
			    url:'http://localhost:9093/scan',
				beforeSend:function(xhr){
				xhr.overrideMimeType('text/plain; charset=x-user-defined');
			    }}).done(function(data, textstatus, jq){
				    console.log(jq);
				});
		});
	    $('#test').click(function(){
		    $.ajax({
			    url:'http://localhost:9093/test',
				beforeSend:function(xhr){
				xhr.overrideMimeType('text/plain; charset=x-user-defined');
			    }}).done(function(data, textstatus, jq){
				    console.log(jq);
				});
		});
		$.get('/dir.json', function(data){
			$.each(data, function(index, d){
				var K=d.substring(d.lastIndexOf('/'), d.length);
				$('#dir').append(new Option(K, d));
			    });
		    });
	    $('#upload').click(function(){
		    var K=[];
		    $('#dir option:selected').each(function(){
			    K.push($(this).val());
			});
		    $.ajax({
			    type:'POST',
				url:'/upload.json',
				data:JSON.stringify({dir:K}),
				contentType:'application/json',
				dataType:'json'});
		});

	};
	
	
	init();
    })();  


