#! /usr/bin/env python

from WebInterfaces.WebHost.WebHost import *
import random
import threading
import time

import random

import traceback

class JeffyWebInterface(WebInterface):
	def __init__(self,port,tox_bot):
		self.port = port
		self.host = WebHost(self.port,staticdir="WebInterfaces/static",staticindex="jeffy.html")
		self.tox_bot = tox_bot
		
		self.connect('/user_stats/',		'USER_STATS',	'GET')
		self.connect('/all_users/',			'ALL_USERS',	'GET')
		self.connect('/best_users/:cnt',	'BEST_USERS',	'GET')
		self.connect('/worst_users/:cnt',	'WORST_USERS',	'GET')
		self.connect('/user_info/:uname',	'USER_INFO',	'GET')
	
	def getAllUsersDict(self):
		return self.tox_bot.get_profiles()
		# return {"ZahmbieND":{"username":"ZahmbieND","worst_messages":[["",1],["",1]],"toxicity":1},"uname":{"username":"uname","worst_messages":[["",1],["",1]],"toxicity":0.9}}
		# return {"ZahmbieND":{"username":"ZahmbieND","worst_messages":[["Hi",1],["Bye",0.999]],"toxicity":1},
		# 	"uname":self.getRandomFakeData("uname"),
		# 	"john effrey":self.getRandomFakeData("john effrey"),
		# 	"chiggin":self.getRandomFakeData("chiggin"),
		# 	"jbaker":self.getRandomFakeData("jbaker"),
		# }
	
	def getUserStatsDict(self):
		return self.tox_bot.get_user_stats()

	def getNeutralFakeData(self,username):
		return {
			"username":username,
			"worst_messages":[],
			"best_messages":[],
			"toxicity":0,
			"num_messages":0,
		}

	def getRandomFakeData(self,username):
		fake_data = self.getNeutralFakeData(username)
		fake_data["toxicity"] = random.random()*2-1
		fake_data["worst_messages"].append(["Message Text",random.random()*2-1])
		fake_data["worst_messages"].append(["Message Text",random.random()*2-1])
		fake_data["worst_messages"].append(["Message Text",random.random()*2-1])
		fake_data["worst_messages"].append(["Message Text",random.random()*2-1])
		fake_data["worst_messages"].append(["Message Text",random.random()*2-1])
		fake_data["best_messages"].append(["Message Text",random.random()*2-1])
		fake_data["best_messages"].append(["Message Text",random.random()*2-1])
		fake_data["best_messages"].append(["Message Text",random.random()*2-1])
		fake_data["best_messages"].append(["Message Text",random.random()*2-1])
		fake_data["best_messages"].append(["Message Text",random.random()*2-1])
		return fake_data

	def getAllUsersList(self):
		user_dict = self.getAllUsersDict()
		user_list = []
		for key in user_dict:
			user_list.append(user_dict[key])
		return user_list
	
	def getUserStatsList(self):
		user_dict = self.getUserStatsDict()
		user_list = []
		for key in user_dict:
			user_list.append(user_dict[key])
		return user_list

	def getSortedUsers(self):
		return sorted(self.getAllUsersList(), key=lambda k: k["toxicity"])

	def getSortedUserStats(self):
		return sorted(self.getUserStatsList(), key=lambda k: k["toxicity"])

	def USER_STATS(self):
		"""return stats on all users"""
		output = {'result':'success'}
		try:
			output["users"] = self.getUserStatsList()
		except Exception as ex:
			output['result'] = 'error'
			output['message'] = str(ex)
			output['traceback'] = traceback.format_exc()
		return json.dumps(output)

	def ALL_USERS(self):
		"""return stats on all users"""
		output = {'result':'success'}
		try:
			output["users"] = self.getSortedUsers()
		except Exception as ex:
			output['result'] = 'error'
			output['message'] = str(ex)
			output['traceback'] = traceback.format_exc()
		return json.dumps(output)
	
	def BEST_USERS(self,cnt):
		"""return stats on the best users"""
		output = {'result':'success'}
		try:
			users = self.getSortedUsers()
			users.reverse()
			output["users"] = users[:int(cnt)]
		except Exception as ex:
			output['result'] = 'error'
			output['message'] = str(ex)
			output['traceback'] = traceback.format_exc()
		return json.dumps(output)
	
	def WORST_USERS(self,cnt):
		"""return stats on the worst users"""
		output = {'result':'success'}
		try:
			output["users"] = self.getSortedUsers()[:int(cnt)]
		except Exception as ex:
			output['result'] = 'error'
			output['message'] = str(ex)
			output['traceback'] = traceback.format_exc()
		return json.dumps(output)
	
	def USER_INFO(self,uname):
		"""return stats on a specific user"""
		output = {'result':'success'}
		try:
			users = self.getAllUsersDict()
			if uname.lower() in users:
				output["stats"] = users[uname.lower()]
			else:
				output["stats"] = self.getNeutralFakeData(uname.lower())
		except Exception as ex:
			output['result'] = 'error'
			output['message'] = str(ex)
			output['traceback'] = traceback.format_exc()
		return json.dumps(output)

	def startWebHost(self):
		self.host.start_service()
	
	def stopWebHost(self):
		self.host.stop_service()
	
	def startRESTinterface(self):
		self.thr = threading.Thread(target=self.startWebHost)
		self.thr.daemon = True
		self.thr.start()
		return self.thr
	
	def stopRESTinterface(self):
		self.stopWebHost()