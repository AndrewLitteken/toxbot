
function restart_svin(dur,acc) {
	WebRequest("GET","/restart_svin/"+dur+"/"+acc,"",function(text) {
		data = JSON.parse(text);
		if(data["result"]=="success") {
			alert("Success!");
		} else {
			alert("ERROR: "+data["message"]+" \nTraceback: "+data["traceback"]);
		}
	},function(err) {
		alert("ERROR: "+err);
	});
}

function restart_svin_clicked() {
	restart_svin(document.getElementById("survey_in_dur").value,document.getElementById("survey_in_acc").value);
}

function load_info() {
	WebRequest("GET","/info/","",function(text) {
		data = JSON.parse(text);
		if(data["result"]=="success") {
			document.getElementById("status_body").innerHTML = '';
			document.getElementById("status_body").appendChild(document.createTextNode(JSON.stringify(data["data"], null, '\t')));
		} else {
			alert("ERROR: "+data["message"]+" \nTraceback: "+data["traceback"]);
		}
		setTimeout('load_info()',1000);
	},function(err) {
		alert("ERROR: "+err);
		setTimeout('load_info()',250);
	});
}

window.onload = function() {
	load_info();
}
