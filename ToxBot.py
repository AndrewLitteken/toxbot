import queue, heapq, threading
from ToneAnalyzer import ToneAnalyzer
from PersonalityAnalyzer import PersonalityAnalyzer

class ToxBot:
	def __init__(self):
		self.messages = Queue.Queue()
		self.personalityQueue = Queue.Queue()
		self.profiles = {}
		self.whitelist = {}
		self.threshold = .6
		self.toxicity = 0

	class Profile:
		def __init__(self, usr, message):
			self.username = usr
			self.numMessages = 1
			self.bad = []
			heappush(self.bad, (message[1], message))
			self.recent = [message]
			self.inQueue = False
			self.personality = None

		def add_message(message, personalityQueue):
			self.recent.add(message)
			heappush(self.bad, (message[1], message))
			while(len(bad) > 10):
				del bad[10]
			self.numMessages += 1
			if self.recent.size() >= 60 and not self.inQueue():
				personalityQueue.put(self)
				self.inQueue = True
		
		def update_personality(self): #, personalityAnalyzer):
			numNewMessages = len(self.recent)
			personality = PersonalityAnalyzer.get_personality(recent)
			self.recent.clear()
			self.inQueue = False
			if self.personality is None:
				self.personality = personality
			else:
				scale = numNewMessages/self.numMessages
				personality = personalityAnalyzer.scale_personalities(personality, self.personality, scale, 1-scale)

	def analyze_tone(self, analyzer, messages, threshold, profiles, whitelist):
		while True:
			while not messages.empty():
				message = messages.get()
				score = analyzer.get_score(message)
				if message[0] in profiles:
					profileMessage = (message[1], score)
					profiles[message[0]].addMessage(profileMessage)
				else:
					if score < -1*threshold :
						if message[0] in whitelist:
							whitelist[message[0]] -= 1
							if whitelist[message[0]] <= 0:
								del whitelist[message[0]]
						else:
							profileMessage = (message[1], score)
							profiles[message[0]] = Profile(message[0], ProfileMessage)
			time.sleep(2)

	def analyze_personality(self, presonalityAnalyzer, personalityQueue):
		while True:
			while not personalityQueue.empty():
				profile = personalityQueue.get()
				profile.update_personaliy()
			time.sleep(2)
	
	def jeffy_listen(self, usr, auth, irc, channel):
		jeffy = IRCbot(usr, auth, irc, channel, self.messages)
		jeffy.listen()
	
	def get_profiles(self):
		profDict = {}
		for prof in self.profiles:
			profInfo = {"username": prof.username, "worst_messages": prof.bad, "toxicity": prof.toxicity}
			profDict[prof.username] = profInfo
		return profDict

	def run(self):
		toneAnalyzer1 = ToneAnalyzer('a54c1a30-92fe-4c1f-b34a-02936047e396', '8WTlVVDHFHCt', '2016-05-19')
		# personalityAnalyzer1 = PersonalityAnalyzer() # What do I need to pass?

		# toneAnalyzer2 = ToneAnalyzer('a54c1a30-92fe-4c1f-b34a-02936047e396', '8WTlVVDHFHCt', '2016-05-19');
		# thread.start_new_thread(analyze_tone, (analyzer2, messages));
		
		toneAnalyzer1 = threading.Thread(target=analyze_tone, args=("johnathonnow", "oauth:mm84kpr5or9rmashwlp9f8dxprqm3b", "irc.chat.twitch.tv", "#summit1g"))
		jeffyThread = threading.Thread(target=jeffy_listen, args=())

		toneAnalyzer1.start()
