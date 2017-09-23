window.auth_data = "";
function get_auth_info() {
	return window.auth_data;
}

function add_auth_body(body) {
	body["auth"] = get_auth_info();
	return body;
}

function get_auth_body() {
	return add_auth_body({});
}

function test_login(callback,err_callback) {
	var body = JSON.stringify(get_auth_body());
	QueuedWebRequest("POST","/login_test/",body,false,function(text) {
		var data = JSON.parse(text);
		if(data["result"]=="success") {
			callback();
		} else {
			console.log("Error logging in: "+data["message"]+" Traceback: "+data["traceback"]);
			err_callback();
		}
	});
}

function create_table(columns,data,click_callback) {
	function create_table_head(columns) {
		var tr = document.createElement('tr');
		for (var i in columns) {
			var col = columns[i]["heading"];
			var txt = col;
			var th_text = document.createTextNode(txt);
			var th = document.createElement('th');
			th.appendChild(th_text);
			tr.appendChild(th);
		}
		return tr;
	}
	function create_table_row(columns,data,click_callback) {
		var tr = document.createElement('tr');
		tr.onclick = function() {
			click_callback(data);
		};
		for (var i in columns) {
			var td = document.createElement('td');
			var td_child = null;
			if(columns[i]["map_func"]!=undefined) {
				td_child = document.createElement("div");
				td_child.appendChild(document.createTextNode("Loading..."));
				columns[i]["map_func"](data,td_child);
			} else {
				var key = columns[i]["key"];
				var txt = data[key];
				td_child = document.createTextNode(txt);
			}
			tr.appendChild(td);
			td.appendChild(td_child);
		}
		return tr;
	}
	
	var table = document.createElement('table');
	table.setAttribute("class","table table-hover");
	var thead = document.createElement('thead');
	var tbody = document.createElement('tbody');
	table.appendChild(thead);
	table.appendChild(tbody);
	var head = create_table_head(columns);
	thead.appendChild(head);
	for (var i in data) {
		var row = create_table_row(columns,data[i],function(new_data) {
			click_callback(new_data);
		});
		tbody.appendChild(row);
	}
	return table;
}

function populate_table(params) {
	var body = JSON.stringify(get_auth_body());
	QueuedWebRequest("POST",params["URL"],body,false,function(text) {
		var data = JSON.parse(text);
		if(data["result"]=="success") {
			var div = document.getElementById(params["div_id"]);
			div.innerHTML = "";
			var table = create_table(params["columns"],data["data"],params["callback"]);
			div.appendChild(table);
		} else {
			console.log("Server error getting data for table\""+params["div_id"]+"\": "+data["message"]+" Traceback: "+data["traceback"]);
		}
	});
}
function populate_all_tables(table_params) {
	for (var i in table_params) {
		populate_table(table_params[i]);
	}
}

function get_user_by_id(id,callback) {
	var body = JSON.stringify(get_auth_body());
	QueuedWebRequest("POST","/get_user_by_id/"+id,body,true,function(text) {
		var data = JSON.parse(text);
		if(data["result"]=="success") {
			callback(data["data"][0]);
		} else {
			console.log("Server error getting data for user #"+id+": "+data["message"]+" Traceback: "+data["traceback"]);
		}
	});
}

function get_vehicle_by_id(id,callback) {
	var body = JSON.stringify(get_auth_body());
	QueuedWebRequest("POST","/get_vehicle_by_id/"+id,body,true,function(text) {
		var data = JSON.parse(text);
		if(data["result"]=="success") {
			callback(data["data"][0]);
		} else {
			console.log("Server error getting data for vehicle #"+id+": "+data["message"]+" Traceback: "+data["traceback"]);
		}
	});
}

function get_fuel_type_by_id(id,callback) {
	var body = JSON.stringify(get_auth_body());
	QueuedWebRequest("POST","/get_fuel_type_by_id/"+id,body,true,function(text) {
		var data = JSON.parse(text);
		if(data["result"]=="success") {
			callback(data["data"][0]);
		} else {
			console.log("Server error getting data for fuel type #"+id+": "+data["message"]+" Traceback: "+data["traceback"]);
		}
	});
}

function io_screen_daemon() {
	function update_io_screen(rows) {
		function string_extend(string,length) {
			if(string.length>length) {
				return string.substring(0,length);
			} else if(string.length==length) {
				return string;
			} else {
				return string_extend(string+' ',length);
			}
		}
		
		var screen = document.getElementById("io_screen");
		screen.innerHTML = "";
		for (var i in rows) {
			if(i>0) {
				var brk = document.createElement('br');
				screen.appendChild(brk);
			}
			var row = rows[i];
			var row_text_node = document.createTextNode(string_extend(row,20).replace(/ /g, '\xa0'));
			screen.appendChild(row_text_node);
		}
	}
	
	var body = JSON.stringify(get_auth_body());
	QueuedWebRequest("POST","/IO/get_lcd/",body,false,function(text) {
		var data = JSON.parse(text);
		if(data["result"]=="success") {
			update_io_screen(data["data"]);
		}
		window.setTimeout(io_screen_daemon,500);
	});
}

function submit_code() {
	var code_input = document.getElementById("code_input");
	var code = code_input.value;
	code_input.value = "";
	if(code=="") {
		code = "0";
	}
	var body = JSON.stringify(get_auth_body());
	WebRequest("POST","/IO/add_code/"+code,body,function(text) {},function(text) {});
}

function refresh_data() {
	var table_params = [
		{
			"div_id":	"pumped_body",
			"URL":		"/get_pumped/",
			"columns":	[
				{
					"heading":"User",
					"map_func":function(data,par){
						get_user_by_id(data["UserID"],function(user){
							par.innerHTML = "";
							par.appendChild(document.createTextNode(user["Name"]));
						});
					},
				},
				{"heading":"User ID",			"key":"UserID",			},
				{
					"heading":"Vehicle",
					"map_func":function(data,par){
						get_vehicle_by_id(data["VehicleID"],function(user){
							par.innerHTML = "";
							par.appendChild(document.createTextNode(user["Name"]));
						});
					},
				},
				{"heading":"Vehicle ID",		"key":"VehicleID",		},
				{
					"heading":"Fuel Type",
					"map_func":function(data,par){
						get_fuel_type_by_id(data["FuelType"],function(user){
							par.innerHTML = "";
							par.appendChild(document.createTextNode(user["Name"]));
						});
					},
				},
				{"heading":"Fuel Type ID",		"key":"FuelType",		},
				{"heading":"Gallons Pumped",	"key":"Gallons",		},
				{"heading":"Modified Date",		"key":"ModifiedDate",	},
				{
					"heading":"Pushed to Server",
					"map_func":function(data,par){
						par.innerHTML = "";
						if(data["UpdateStatus"]==1) {
							par.appendChild(document.createTextNode("True"));
						} else {
							par.appendChild(document.createTextNode("False"));
						}
					},
				},
				{"heading":"Reccnt",			"key":"Reccnt",			},
			],
			"callback":	function(data){console.log(data);},
		},
		{
			"div_id":	"user_body",
			"URL":		"/get_user/",
			"columns":	[
				{"heading":"Name",				"key":"Name",			},
				{"heading":"Passcode",			"key":"Passcode",		},
				{
					"heading":"Allowed",
					"map_func":function(data,par){
						par.innerHTML = "";
						if(data["Allowed"]==1) {
							par.appendChild(document.createTextNode("True"));
						} else {
							par.appendChild(document.createTextNode("False"));
						}
					},
				},
				{"heading":"ID",				"key":"ID",				},
				{"heading":"CreatedDate",		"key":"CreatedDate",	},
				{"heading":"Origin",			"key":"Origin",			},
				{"heading":"ModifiedDate",		"key":"ModifiedDate",	},
				{"heading":"ModifiedOn",		"key":"ModifiedOn",		},
				{
					"heading":"Pushed to Server",
					"map_func":function(data,par){
						par.innerHTML = "";
						if(data["UpdateStatus"]==1) {
							par.appendChild(document.createTextNode("True"));
						} else {
							par.appendChild(document.createTextNode("False"));
						}
					},
				},
				{"heading":"Reccnt",			"key":"Reccnt",			},
			],
			"callback":	user_popup,
		},
		{
			"div_id":	"vehicle_body",
			"URL":		"/get_vehicle/",
			"columns":	[
				{"heading":"Name",				"key":"Name",			},
				{"heading":"Passcode",			"key":"Passcode",		},
				{
					"heading":"Allowed",
					"map_func":function(data,par){
						par.innerHTML = "";
						if(data["Allowed"]==1) {
							par.appendChild(document.createTextNode("True"));
						} else {
							par.appendChild(document.createTextNode("False"));
						}
					},
				},
				{"heading":"ID",				"key":"ID",				},
				{"heading":"CreatedDate",		"key":"CreatedDate",	},
				{"heading":"Origin",			"key":"Origin",			},
				{"heading":"ModifiedDate",		"key":"ModifiedDate",	},
				{"heading":"ModifiedOn",		"key":"ModifiedOn",		},
				{
					"heading":"Pushed to Server",
					"map_func":function(data,par){
						par.innerHTML = "";
						if(data["UpdateStatus"]==1) {
							par.appendChild(document.createTextNode("True"));
						} else {
							par.appendChild(document.createTextNode("False"));
						}
					},
				},
				{"heading":"Reccnt",			"key":"Reccnt",			},
			],
			"callback":	vehicle_popup,
		},
		{
			"div_id":	"fuel_type_body",
			"URL":		"/get_fuel_type/",
			"columns":	[
				{"heading":"Name",				"key":"Name",			},
				{"heading":"Passcode",			"key":"Passcode",		},
				{
					"heading":"Allowed",
					"map_func":function(data,par){
						par.innerHTML = "";
						if(data["Allowed"]==1) {
							par.appendChild(document.createTextNode("True"));
						} else {
							par.appendChild(document.createTextNode("False"));
						}
					},
				},
				{"heading":"ID",				"key":"ID",				},
				{"heading":"RelayPin",			"key":"RelayPin",		},
				{"heading":"PulsePin",			"key":"PulsePin",		},
				{"heading":"CreatedDate",		"key":"CreatedDate",	},
				{"heading":"Origin",			"key":"Origin",			},
				{"heading":"ModifiedDate",		"key":"ModifiedDate",	},
				{"heading":"ModifiedOn",		"key":"ModifiedOn",		},
				{
					"heading":"Pushed to Server",
					"map_func":function(data,par){
						par.innerHTML = "";
						if(data["UpdateStatus"]==1) {
							par.appendChild(document.createTextNode("True"));
						} else {
							par.appendChild(document.createTextNode("False"));
						}
					},
				},
				{"heading":"Reccnt",			"key":"Reccnt",			},
			],
			"callback":	fuel_type_popup,
		},
	];
	populate_all_tables(table_params);
}

function popup_hide() {
	var popup = document.getElementById("popup");
	popup.style.display = "none";
}
function popup(title,body) {
	var popup = document.getElementById("popup");
	var popup_title = document.getElementById("popup_title");
	var popup_body = document.getElementById("popup_body");
	var title_text = document.createTextNode(title);
	popup_title.innerHTML = "";
	popup_body.innerHTML = "";
	popup_title.appendChild(title_text);
	popup_body.appendChild(body);
	popup.style.display = "block";
}

function make_input(label,id,value) {
	var group = document.createElement("div");
	group.setAttribute("class","form-group");
	var label_elem = document.createElement("label");
	label_elem.setAttribute("class","col-lg-2 control-label");
	label_elem.setAttribute("for",id);
	label_elem.appendChild(document.createTextNode(label));
	group.appendChild(label_elem);
	var col = document.createElement("div");
	col.setAttribute("class","col-lg-10");
	var input = document.createElement("input");
	input.setAttribute("class","form-control");
	input.setAttribute("id",id);
	input.setAttribute("type","text");
	input.setAttribute("value",value);
	col.appendChild(input);
	group.appendChild(col);
	return group;
}
function make_checkbox(label,check_label,id,value,callback) {
	var group = document.createElement("div");
	group.setAttribute("class","form-group");
	var label_elem = document.createElement("label");
	label_elem.setAttribute("class","col-lg-2 control-label");
	label_elem.setAttribute("for",id+"_div");
	label_elem.appendChild(document.createTextNode(label));
	group.appendChild(label_elem);
	var col = document.createElement("div");
	col.setAttribute("class","col-lg-10");
	var div = document.createElement("div");
	var input = document.createElement("input");
	input.setAttribute("id",id);
	input.setAttribute("type","checkbox");
	input.checked = value;
	input.onclick = function() {
		if(callback!=null) {
			callback(input.checked);
		}
	};
	var label_elem_2 = document.createElement("label");
	div.setAttribute("class","checkbox");
	div.setAttribute("id",id+"_div");
	label_elem_2.appendChild(input);
	label_elem_2.appendChild(document.createTextNode(check_label));
	div.appendChild(label_elem_2);
	col.appendChild(div);
	group.appendChild(col);
	return group;
}

function make_button(text,id,callback) {
	var group = document.createElement("div");
	group.setAttribute("class","form-group");
	var col = document.createElement("div");
	col.setAttribute("class","col-lg-10 col-lg-offset-2");
	var div = document.createElement("div");
	var input = document.createElement("button");
	input.setAttribute("id",id);
	input.setAttribute("class","btn btn-primary");
	input.appendChild(document.createTextNode(text));
	input.onclick = function() {
		if(callback!=null) {
			callback();
		}
	};
	col.appendChild(input);
	group.appendChild(col);
	return group;
}

function user_popup(data) {
	if(data==null) {
		data = {
			"Name":"",
			"Passcode":"",
			"Allowed":false,
			"ID":"",
			"set_id":false,
		}
	} else {
		data["set_id"] = true;
	}
	var div = document.createElement("div");
	div.setAttribute("class","form-horizontal");
	div.appendChild(make_input("Name","user_name",data["Name"]));
	div.appendChild(make_input("Passcode","user_passcode",data["Passcode"]));
	div.appendChild(make_checkbox("Allowed","allowed to pump fuel","user_allowed",data["Allowed"],null));
	var selected_user_id = data["set_id"];
	var user_id_input = make_input("User ID","user_id",data["ID"]);
	function user_id_selecting(value) {
		selected_user_id = value;
		if(selected_user_id) {
			user_id_input.style.display = "block";
		} else {
			user_id_input.style.display = "none";
		}
	}
	user_id_selecting(selected_user_id);
	div.appendChild(make_checkbox("Create or Update","update existing record","user_id_select",selected_user_id,user_id_selecting));
	div.appendChild(user_id_input);
	div.appendChild(make_button("Submit","user_submit_button",function() {
		var new_data = {
			"Name":document.getElementById("user_name").value,
			"Passcode":document.getElementById("user_passcode").value,
			"Allowed":document.getElementById("user_allowed").checked,
		}
		if(document.getElementById("user_id_select").checked) {
			new_data["ID"] = document.getElementById("user_id").value;
			var body = JSON.stringify(add_auth_body(new_data));
			QueuedWebRequest("POST","/update_user/",body,false,function(text) {
				var ret = JSON.parse(text);
				if(ret["result"]=="success") {
					popup_hide();
					refresh_data();
				}
			});
		} else {
			var body = JSON.stringify(add_auth_body(new_data));
			QueuedWebRequest("POST","/add_user/",body,false,function(text) {
				var ret = JSON.parse(text);
				if(ret["result"]=="success") {
					popup_hide();
					refresh_data();
				}
			});
		}
	}));
	popup("Change or create user",div);
}

function vehicle_popup(data) {
	if(data==null) {
		data = {
			"Name":"",
			"Passcode":"",
			"Allowed":false,
			"ID":"",
			"set_id":false,
		}
	} else {
		data["set_id"] = true;
	}
	var div = document.createElement("div");
	div.setAttribute("class","form-horizontal");
	div.appendChild(make_input("Name","vehicle_name",data["Name"]));
	div.appendChild(make_input("Passcode","vehicle_passcode",data["Passcode"]));
	div.appendChild(make_checkbox("Allowed","allowed to pump fuel","vehicle_allowed",data["Allowed"],null));
	var selected_vehicle_id = data["set_id"];
	var vehicle_id_input = make_input("Vehicle ID","vehicle_id",data["ID"]);
	function vehicle_id_selecting(value) {
		selected_vehicle_id = value;
		if(selected_vehicle_id) {
			vehicle_id_input.style.display = "block";
		} else {
			vehicle_id_input.style.display = "none";
		}
	}
	vehicle_id_selecting(selected_vehicle_id);
	div.appendChild(make_checkbox("Create or Update","update existing record","vehicle_id_select",selected_vehicle_id,vehicle_id_selecting));
	div.appendChild(vehicle_id_input);
	div.appendChild(make_button("Submit","vehicle_submit_button",function() {
		var new_data = {
			"Name":document.getElementById("vehicle_name").value,
			"Passcode":document.getElementById("vehicle_passcode").value,
			"Allowed":document.getElementById("vehicle_allowed").checked,
		}
		if(document.getElementById("vehicle_id_select").checked) {
			new_data["ID"] = document.getElementById("vehicle_id").value;
			var body = JSON.stringify(add_auth_body(new_data));
			QueuedWebRequest("POST","/update_vehicle/",body,false,function(text) {
				var ret = JSON.parse(text);
				if(ret["result"]=="success") {
					popup_hide();
					refresh_data();
				}
			});
		} else {
			var body = JSON.stringify(add_auth_body(new_data));
			QueuedWebRequest("POST","/add_vehicle/",body,false,function(text) {
				var ret = JSON.parse(text);
				if(ret["result"]=="success") {
					popup_hide();
					refresh_data();
				}
			});
		}
	}));
	popup("Change or create vehicle",div);
}

function fuel_type_popup(data) {
	if(data==null) {
		data = {
			"Name":"",
			"Passcode":"",
			"Allowed":false,
			"ID":"",
			"RelayPin":"",
			"PulsePin":"",
			"set_id":false,
		}
	} else {
		data["set_id"] = true;
	}
	var div = document.createElement("div");
	div.setAttribute("class","form-horizontal");
	div.appendChild(make_input("Name","fuel_type_name",data["Name"]));
	div.appendChild(make_input("Passcode","fuel_type_passcode",data["Passcode"]));
	div.appendChild(make_checkbox("Allowed","allowed to be used","fuel_type_allowed",data["Allowed"],null));
	div.appendChild(make_input("Relay Pin","fuel_type_relay_pin",data["RelayPin"]));
	div.appendChild(make_input("Pulse Pin","fuel_type_pulse_pin",data["PulsePin"]));
	var selected_fuel_type_id = data["set_id"];
	var fuel_type_id_input = make_input("Fuel Type ID","fuel_type_id",data["ID"]);
	function fuel_type_id_selecting(value) {
		selected_fuel_type_id = value;
		if(selected_fuel_type_id) {
			fuel_type_id_input.style.display = "block";
		} else {
			fuel_type_id_input.style.display = "none";
		}
	}
	fuel_type_id_selecting(selected_fuel_type_id);
	div.appendChild(make_checkbox("Create or Update","update existing record","fuel_type_id_select",selected_fuel_type_id,fuel_type_id_selecting));
	div.appendChild(fuel_type_id_input);
	div.appendChild(make_button("Submit","fuel_type_submit_button",function() {
		var new_data = {
			"Name":document.getElementById("fuel_type_name").value,
			"Passcode":document.getElementById("fuel_type_passcode").value,
			"Allowed":document.getElementById("fuel_type_allowed").checked,
			"RelayPin":document.getElementById("fuel_type_relay_pin").value,
			"PulsePin":document.getElementById("fuel_type_pulse_pin").checked,
		}
		if(document.getElementById("fuel_type_id_select").checked) {
			new_data["ID"] = document.getElementById("fuel_type_id").value;
			var body = JSON.stringify(add_auth_body(new_data));
			QueuedWebRequest("POST","/update_fuel_type/",body,false,function(text) {
				var ret = JSON.parse(text);
				if(ret["result"]=="success") {
					popup_hide();
					refresh_data();
				}
			});
		} else {
			var body = JSON.stringify(add_auth_body(new_data));
			QueuedWebRequest("POST","/add_fuel_type/",body,false,function(text) {
				var ret = JSON.parse(text);
				if(ret["result"]=="success") {
					popup_hide();
					refresh_data();
				}
			});
		}
	}));
	popup("Change or create fuel type",div);
}

function login(callback) {
	var div = document.createElement("div");
	div.setAttribute("class","form-horizontal");
	div.appendChild(make_input("Username","login_username",""));
	div.appendChild(make_input("Password","login_password",""));
	div.appendChild(make_button("Submit","login_submit_button",function() {
		window.auth_data = {
			"username":document.getElementById("login_username").value,
			"password":document.getElementById("login_password").value,
		}
		test_login(function() {
			popup_hide();
			callback();
		},function() {});
	}));
	popup("Login",div);
	document.getElementById("login_password").setAttribute("type","password");
}

function init() {
	login(function() {
		refresh_data();
		io_screen_daemon();
	});
}

init();
