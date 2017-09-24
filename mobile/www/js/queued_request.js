
window.web_request_cache = {};
window.web_request_queue = [];
window.web_request_queue_running = false;
function QueuedWebRequest(HTTP_type,URL,body,cached,callback) {
	function request_queue_handler() {
		if(window.web_request_queue.length>0) {
			var item = window.web_request_queue[0];
			var cachekey = item['cachekey'];
			var info = item['info'];
			if((cachekey in window.web_request_cache) && info['cached']) {
				info['callback'](window.web_request_cache[cachekey]);
				window.web_request_queue = window.web_request_queue.splice(1,window.web_request_queue.length);
				request_queue_handler();
			} else {
				WebRequest(info['HTTP_type'],info['URL'],info['body'],function(text) {
					if(info['cached']) {
						window.web_request_cache[cachekey] = text;
					}
					info['callback'](text);
					window.web_request_queue = window.web_request_queue.splice(1,window.web_request_queue.length);
					window.setTimeout(request_queue_handler,100);
				},function(text) {
					console.log("Error: \""+text+"\" with request "+info['HTTP_type']+' '+info['URL']+' Body:'+info['body']);
					window.web_request_queue = window.web_request_queue.splice(1,window.web_request_queue.length).concat([window.web_request_queue.splice[1]]);
					window.setTimeout(request_queue_handler,100);
				});
			}
		} else {
			window.setTimeout(request_queue_handler,100);
		}
	}
	
	if (!window.web_request_queue_running) {
		window.web_request_queue_running = true;
		request_queue_handler();
	}
	
	function getcachekey(info) {
		return "[[HTTP_type]"+info['HTTP_type']+"][[URL]"+info['URL']+"][[body]"+info['body']+"]";
	}
	
	
	var info = {
		'HTTP_type':HTTP_type,
		'URL':URL,
		'body':body,
		'cached':cached,
		'callback':callback,
	};
	var cachekey = getcachekey(info);
	if ((cachekey in window.web_request_cache) && cached) {
		callback(window.web_request_cache[cachekey]);
	} else {
		window.web_request_queue.push({
			'cachekey':cachekey,
			'info':info,
		});
	}
}

