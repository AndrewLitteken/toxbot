#! /usr/bin/env python

# TestInterface.py
# implements a generic test web interface for cherrypy
# made by Joshua Huseman, jhuseman@nd.edu
# 06/08/2016

import cherrypy
from WebHost import *
# from WebInterface import *
import json

import random

class TestInterface(WebInterface):
	def __init__(self):
		self.host = WebHost(80)
		self.connect('/test/:id/:it','GET_ID','GET')
		self.host.start_service()
		
	
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
	TestInterface()