#! /usr/bin/env python

# WebHost.py
# defines:
#	WebHost:
#		cherrypy wrapper for hosting a "/static" folder
#		allows WebInterface objects to serve dynamic content
#		  alongside the "/static" folder
#	WebInterface:
#		"purely virtual" class for a dynamic web interface
#
# made by Joshua Huseman, jhuseman@nd.edu
# Created: 06/08/2016
# Updated: 06/13/2016
# Updated: 08/01/2017 - removed logging to screen

import cherrypy
import json
import os

class WebHost(object):
	def __init__(self,port,staticdir="static",staticindex="index.html"):
		self.port = port
		self.dispatcher = cherrypy.dispatch.RoutesDispatcher()
		self.conf = {
			'global' : {
				'server.socket_host': '0.0.0.0',
				'server.socket_port': self.port,
				'log.screen' : False, # Remove these 3 lines to re-enable logging of data to the screen
				'log.access_file': '',
				'log.error_file': '',
				'engine.autoreload.on': False, # Remove this line to re-enable auto-reload
			},
			'/' : {
				'request.dispatch': self.dispatcher,
			},
			'/static' : {
				'tools.staticdir.on':True,
				'tools.staticdir.root':os.getcwd(),
				'tools.staticdir.dir':staticdir,
				'tools.staticdir.index':staticindex,
			},
		}
		cherrypy.config.update(self.conf)
		self.app = cherrypy.tree.mount(None, config=self.conf)

		self.resource_list = []
		WebDocs(self)

	def start_service(self):
		# # output resource list (for debug)
		# print "All Resources:"
		# print self.resource_list
		cherrypy.quickstart(self.app)
	
	def stop_service(self):
		cherrypy.engine.exit()

	def get_dispatcher(self):
		return self.dispatcher

	def log_connection(self,interface,resource,action,method):
		log_entry = {
			"docstring":getattr(interface,action).__doc__,
			"function_name":getattr(interface,action).__name__,
			"resource":resource,
			"method":method,
		}
		self.resource_list.append(log_entry)

class WebInterface(object):
	"""
	Allows for easily defining web interfaces for the server.

	Expects the variable "self.host" to be set to a WebHost
	object before calling "connect()".

	Example __init__ code:
		self.host = WebHost(80)
		self.connect('/test/:id','GET_ID','GET')
		self.host.start_service()
		# starts a WebHost on port 80 that calls member function
		# GET_ID() with the argument after "/test/" when a GET
		# request is received for "/test/<any text here>"
	"""
	def connect(self,resource,action,method):
		"""
		connects a specified action (function) in this object
		to the specified resource (URL)
		and http method (GET/PUT/POST/DELETE)
		"""
		iface_name = resource+'_'+action+'_'+method
		self.dispatcher = self.host.get_dispatcher()
		self.dispatcher.connect(
			iface_name, resource,
			controller=self, action=action,
			conditions=dict(method=[method])
		)
		# log this connection on the host
		self.host.log_connection(self,resource,action,method)

class WebDocs(WebInterface):
	def __init__(self,host):
		self.host = host
		self.connect('/','ROOT_REDIRECT','GET')
		self.connect('/docs/','GET_DOCS','GET')
		self.connect('/docs/json/','GET_DOCS_JSON','GET')

	def ROOT_REDIRECT(self):
		"""redirects to /static/ directory"""
		return """
			<!DOCTYPE html>
			<html>
				<head>
					<META http-equiv="refresh" content="0;URL=/static/">
					<title>WebHost Redirect</title>
				</head>
				<body>
					There is no information at this page.
					If you are not redirected to /static/ immediately, you can click <a href="/static/">here</a>.
					<script>
						window.location = "/static/";
						window.location.replace("/static/");
						window.location.href = "/static/";
					</script>
				</body>
			</html>
		"""

	def GET_DOCS(self):
		"""return this documentation page in HTML format"""
		resources = ""
		for resource in self.host.resource_list:
			resource_html = """
				<tr>
					<td><a href="{resource}">{resource}</a></td>
					<td>{method}</td>
					<td>{function_name}</td>
					<td>{docstring}</td>
				</tr>
			""".format(
				resource = resource["resource"],
				method = resource["method"],
				function_name = resource["function_name"],
				docstring = resource["docstring"],
			)
			resources = resources+resource_html
		return """
			<!DOCTYPE html>
			<html>
				<head>
					<title>WebHost Documentation</title>
				</head>
				<body>
					<table border="1">
						<tr>
							<th>Resource</th>
							<th>Method</th>
							<th>Function Name</th>
							<th>Docstring</th>
						</tr>
						{resources}
					</table>
				</body>
			</html>
		""".format(resources=resources)

	def GET_DOCS_JSON(self):
		"""return this documentation page in JSON format"""
		return json.dumps(self.host.resource_list)

if __name__ == '__main__':
	"""
	serves only a static folder in the local 'static' directory
	"""
	host = WebHost(80)
	host.start_service()
