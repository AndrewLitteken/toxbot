#! /usr/bin/env python

# TestInterface.py
# implements a generic test web interface for cherrypy
# made by Joshua Huseman, jhuseman@nd.edu
# Created: 06/08/2016
# Updated: 06/08/2016

import cherrypy
from WebHost import *
import json

import random

class TestInterface(WebInterface):
	def __init__(self,host):
		self.host = host
		self.connect('/test/:id/:it','GET_ID','GET')
	
	def GET_ID(self,id,it):
		output = {'result':'success'}
		try:
			output['id'] = id
			output['it'] = it
			output['rand'] = random.random()
		except Exception as ex:
			output['result'] = 'error'
			output['message'] = str(ex)
		return json.dumps(output, encoding='latin-1')

if __name__ == '__main__':
	host = WebHost(80)
	TestInterface(host)
	host.start_service()
	
