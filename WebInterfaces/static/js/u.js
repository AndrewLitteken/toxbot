function update_user_stats(classes) {
	var tosend = { "children": classes };

	//tosend.children.push({"name": "andrews", "toxicity": -1, "size": 29});
	tosend.children[0].toxicity = 1 - Math.random() * 2;
	tosend.children[1].size += 2;
	tosend.children[2].size += 4;
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
function download_user_stats() {
	WebRequest("GET", "/user_stats/", "", function (text) {
		var data = JSON.parse(text);
		if (data["result"] == "success") {
			update(data["users"]);
		} else {
			console.log("ERROR: " + data["message"] + " \nTraceback: " + data["traceback"]);
		}
	}, function (err) {
		console.log("ERROR: " + err);
	});
}
setInterval("download_user_stats()", 4000);