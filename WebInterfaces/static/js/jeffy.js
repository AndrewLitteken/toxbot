
function float2goodstring(num) {
	return num.toPrecision(2);
}

function num2color(num) {
	var red = 255*((-1*num/2.0)+0.5);
	var green = 255*((num/2.0) + 0.5);
	var blue = 255*(0);
	var combined = Math.floor(red)*256*256+Math.floor(green)*256+Math.floor(blue);
	var combined_str = (combined + 256*256*256).toString(16);
	combined_str_short = combined_str.substr(combined_str.length-6,6);
	var color="#"+combined_str_short;
	return color;
}

function create_badge(num) {
	var badge = document.createElement("span");
	badge.setAttribute("class","badge");
	badge.appendChild(document.createTextNode(float2goodstring(num)));
	badge.style.backgroundColor=num2color(num);
	badge.style.color = "black";
	return badge;
}

function create_comment_list_item(item) {
	var list_item_elem = document.createElement("li");
	list_item_elem.setAttribute("class","list-group-item");
	list_item_elem.appendChild(create_badge(item[1]));
	list_item_elem.appendChild(document.createTextNode(item[0]));
	return list_item_elem;
}

function create_comment_list(comments) {
	var list_elem = document.createElement("ul");
	list_elem.setAttribute("class","list-group");
	for(var i=0;i<comments.length;i++) {
		list_elem.appendChild(create_comment_list_item(comments[i]));
	}
	return list_elem;
}

function create_user_info_obj(data, is_panel) {
	var ret = document.createElement("div");
	if(is_panel) {
		ret.setAttribute("class","panel panel-default");
	} else {
		ret.setAttribute("class","list-group-item");
	}
	var name_elem;
	if(is_panel) {
		name_elem = document.createElement("div");
		name_elem.setAttribute("class","panel-heading");
	} else {
		name_elem = document.createElement("h4");
		name_elem.setAttribute("class","list-group-item-heading");
	}
	name_elem.appendChild(document.createTextNode(data["username"]));
	name_elem.appendChild(create_badge(data["toxicity"]));
	ret.appendChild(name_elem);
	var sub_elem = document.createElement("div");
	if(is_panel) {
		sub_elem.setAttribute("class","panel-body");
	} else {
		sub_elem.setAttribute("class","list-group-item-text");
	}
	sub_elem.appendChild(create_comment_list(data["worst_messages"]));
	ret.appendChild(sub_elem);
	return ret;
}

function create_user_info_list(data_list) {
	var list_elem = document.createElement("div");
	list_elem.setAttribute("class","list-group");
	for(var i=0;i<data_list.length;i++) {
		var item = data_list[i];
		list_elem.appendChild(create_user_info_obj(item,false));
	}
	return list_elem;
}

function get_user_info(uname) {
	WebRequest("GET","/user_info/"+uname,"",function(text) {
		var data = JSON.parse(text);
		if(data["result"]=="success") {
			var replace = document.getElementById("single_user");
			replace.innerHTML = '';
			replace.appendChild(create_user_info_obj(data["stats"],true));
		} else {
			console.log("ERROR: "+data["message"]+" \nTraceback: "+data["traceback"]);
		}
	},function(err) {
		alert("ERROR: "+err);
	});
}

function get_user_list() {
	var keys = ["user_list_selection_all","user_list_selection_worst","user_list_selection_best"];
	var user_value = "";
	for(var i=0;i<keys.length;i++) {
		if(document.getElementById(keys[i]).checked) {
			user_value = document.getElementById(keys[i]).value;
		}
	}
	var quantity_str = document.getElementById("user_list_quantity").value;
	if(quantity_str=="") {
		quantity_str = "10";
	}
	if(user_value=="all_users") {
		quantity_str = "";
	}
	WebRequest("GET","/"+user_value+"/"+quantity_str,"",function(text) {
		var data = JSON.parse(text);
		if(data["result"]=="success") {
			var replace = document.getElementById("user_list");
			replace.innerHTML = '';
			replace.appendChild(create_user_info_list(data["users"]));
		} else {
			console.log("ERROR: "+data["message"]+" \nTraceback: "+data["traceback"]);
		}
	},function(err) {
		alert("ERROR: "+err);
	});
}
get_user_list();

function get_user_info_submitted() {
	get_user_info(document.getElementById("single_user_select_uname").value);
}
document.getElementById("single_user_select_submit").addEventListener("click",get_user_info_submitted);
document.getElementById("single_user_select_uname").addEventListener("submit",get_user_info_submitted);
document.getElementById("user_list_selection").addEventListener("change",get_user_list);
document.getElementById("user_list_quantity").addEventListener("change",get_user_list);
