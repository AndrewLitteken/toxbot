function update_user_stats(classes) {
	var tosend = { "children": classes };
	changebubble(tosend);
}


// var classes = [
// 	{ "name": "jeffrey2", "toxicity": -1, "size": 4 },
// 	{ "name": "jeffrey", "toxicity": 0, "size": 4 },
// 	{ "name": "huseman", "toxicity": -1, "size": 2 },
// 	{ "name": "andrew", "toxicity": 1, "size": 9 },
// 	{ "name": "andrew2", "toxicity": -.8, "size": 9 },
// 	{ "name": "andrew3", "toxicity": -.6, "size": 9 },
// 	{ "name": "andrew4", "toxicity": -.4, "size": 9 },
// 	{ "name": "andrew5", "toxicity": -.2, "size": 9 },
// 	{ "name": "andrew6", "toxicity": 0, "size": 9 },
// 	{ "name": "andrew7", "toxicity": .2, "size": 9 },
// 	{ "name": "andrew3", "toxicity": .4, "size": 91 },
// 	{ "name": "andrew4", "toxicity": .5, "size": 12 },
// 	{ "name": "andrew5", "toxicity": .7, "size": 15 },
// 	{ "name": "andrew6", "toxicity": .8, "size": 17 },
// 	{ "name": "andrew7", "toxicity": 1, "size": 19 },
// ];
function get_user_stats(finished_callback) {
	QueuedWebRequest("GET", "/user_stats/", "",false, function (text) {
		var data = JSON.parse(text);
		if (data["result"] == "success") {
			update_user_stats(data["users"].slice(0,60));
		} else {
			console.log("ERROR: " + data["message"] + " \nTraceback: " + data["traceback"]);
		}
		finished_callback(data["result"] == "success");
	});
}
