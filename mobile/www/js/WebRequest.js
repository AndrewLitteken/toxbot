function WebRequest(HTTP_type,URL,body,callback,error_callback) {
    URL = "http://10.13.230.88"+URL    
	xhr = new XMLHttpRequest();
	xhr.open(HTTP_type, URL, true);
	xhr.onloadend = function(e) {
		if(xhr.readyState == 4) {
            console.log(URL);
            console.log(xhr.responseText);
			callback(xhr.responseText);
		} else {
			error_callback('Request called onload before ready! readyState:' + xhr.readyState.toString() + ' responseText:' + xhr.responseText);
		}
	};
	// xhr.ontimeout = function(e) {
		// error_callback('timeout: '+xhr.statusText);
	// };
	// xhr.onabort = function(e) {
		// error_callback('aborted: '+xhr.statusText);
	// };
	// xhr.onerror = function(e) {
		// error_callback('error: '+xhr.statusText);
	// };
	xhr.send(body);
}
