#! /usr/bin/env python

# WebInterface.py
#########################################################
#########################################################
#DEPRECATED!! NOW INCLUDED IN WebHost.py
#########################################################
#########################################################
# virtual class for a generic web interface for cherrypy
# made by Joshua Huseman, jhuseman@nd.edu
# 06/08/2016

import cherrypy
from WebHost import *

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
		
	

if __name__ == '__main__':
	print "This file is intended to be 'purely virtual' and included by another file"
	
