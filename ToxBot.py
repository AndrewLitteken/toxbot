#!/usr/bin/env python3

import queue, heapq, threading
from ircbot import IRCbot
from ToneAnalyzer import ToneAnalyzer
from PersonalityAnalyzer import PersonalityAnalyzer
from TranslationModule import TranslationModule
from WebInterfaces.JeffyWebInterface import JeffyWebInterface
import time
import sys


class ToxBot:
    def __init__(self):
        self.toBeTranslated = queue.Queue()
        self.messages = queue.Queue()
        self.personalityQueue = queue.Queue()
        self.profiles = {}
        self.whitelist = {}
        self.threshold = -.5
        self.toxicity = 0

    class Profile:
        def __init__(self, usr, message):
            self.username = usr
            self.numMessages = 1
            self.bad = []
            self.good = []
            heapq.heappush(self.bad, (message[1], message))
            heapq.heappush(self.good, (-1*(message[1]), message))
            self.recent = [message]
            self.inQueue = False
            self.toxicity = None

        def add_message(self, message, personalityQueue):
            """
            adds a message that a person sent to their profile
            :param message: tuple with (message_text, score)
            :param personalityQueue: queue that contains profiles that need a personality analysis
            :return: None
            """
            self.recent.append(message)
            heapq.heappush(self.bad, (message[1], message))
            while len(self.bad) > 3:  # only keeps the worst 3 messages
                del self.bad[3]
            heapq.heappush(self.good, (-1*message[1], message))
            while len(self.good) > 3:  # only keeps the best 3 messages
                del self.good[3]
            self.numMessages += 1
            if len(self.recent) >= 3 and not self.inQueue:  # run a personality analysis every x messages
                personalityQueue.put(self)
                self.inQueue = True

        def update_personality(self, personalityAnalyzer):
            """
            sends a person's personality to be analyzed and updates their toxicity score accordingly
            :param personalityAnalyzer: instance of a personality analyzer, used to analyze the personality
            :return: None
            """
            num_new_messages = len(self.recent)
            total = 0
            for message in self.recent:
                total += message[1]
            tone_tox = total/num_new_messages
            personality_tox = personalityAnalyzer.analyze_personality(self.recent)
            new_tox = (tone_tox+personality_tox)/2
            self.recent.clear()
            self.inQueue = False
            if self.toxicity is None:  # if there have been no prior analyses, toxicity is based on this analysis only
                self.toxicity = new_tox
            else:  # if there have been prior analyses, then add this to total analysis as an average
                scale = num_new_messages / self.numMessages
                self.toxicity = self.toxicity*scale + new_tox*(1-scale)

    def analyze_tone(self, analyzer):
        """
        Thread function, monitors a queue for new messages, if there are messages, analyzes them for tone and creates or
        adds them to a profile
        :param analyzer: instance of a tone analyzer class, used to analyze the tone of the messages pulled from the queue
        :return: None
        """
        while True:
            try:
                while not self.messages.empty():
                    message = self.messages.get()
                    score = analyzer.get_score(message[1])
                    # if score < self.threshold:
                    #     print("\t\t\t" + str(message), " toxicity: " + score)
                    if message[0] in self.profiles:  # if the profile exists, add the message to the profile
                        profile_message = (message[1], score)
                        self.profiles[message[0]].add_message(profile_message, self.personalityQueue)
                    else:  # if the profile does not exist, create a profile with this message as the first
                        profile_message = (message[1], score)
                        self.profiles[message[0]] = self.Profile(message[0], profile_message)
                time.sleep(1)
            except Exception:
                pass

    def analyze_personality(self, analyzer):
        """
        Thread function, monitors a queue for new profiles to analyze the personality for
        :param analyzer: instance of a tone analyzer class, used to analyze the personality of a profile pulled from the queue
        :return: None
        """
        while True:
            while not self.personalityQueue.empty():
                profile = self.personalityQueue.get()
                profile.update_personality(analyzer)
            time.sleep(3)

    def jeffy_listen(self, usr, auth, irc, channel):
        """
        Thread function, sets the thread to listen to the twitch chat and update to the messages queue
        :param usr: the username on twitch
        :param auth: the oauth token for the user on twitch
        :param irc: the name of the irc channel
        :param channel: the name of the channel on twitch
        :return: None
        """
        self.jeffy = IRCbot(usr, auth, irc, channel, self.toBeTranslated)
        self.jeffy.listen()

    def get_profiles(self):
        """
        creates and returns a dictionary of profiles for the web application
        :return: dictionary of users to their worst 10 messages and their overall toxicity
        """
        profDict = {}
        for key in self.profiles:
            prof = self.profiles[key]
            bad = []
            good = []
            for item in prof.bad:
                bad.append(list(item[1]))
            for item in prof.good:
                good.append(list(item[1]))
            toxicity = prof.toxicity
            if toxicity is None:
                toxicity = 0
            profInfo = {"username": prof.username,
                        "worst_messages": bad,
                        "best_messages": good,
                        "toxicity": toxicity,
                        "num_messages": prof.numMessages}
            profDict[prof.username] = profInfo
        return profDict

    def run(self, channel):
        """
        Creates the instantiations of the analyzer classes, creates and starts the threads
        :return: None
        """
        tone_analyzer = ToneAnalyzer('15995331-bf1f-4ca7-9a79-4b1ae9c5d544', 'hnioI4YAvFbn', '2016-05-19',
                                     "./data/all_marked_data.txt", "./data/all_marked_data_scores.txt", False)
        personality_analyzer = PersonalityAnalyzer('d68b1f5b-c43d-4b0d-a644-775e1071194e', 'fJMpsSvXYBIF', '2016-9-20')
        language_analyzer = TranslationModule('5a26e50e-a391-451f-9cbe-830f84052ad7', 'dQmWGtOGWeFV')

        tone_analyzer_thread = threading.Thread(target=self.analyze_tone, args=(tone_analyzer,))
        jeffy_thread = threading.Thread(target=self.jeffy_listen, args=("johnathonnow", "oauth:mm84kpr5or9rmashwlp9f8dxprqm3b", "irc.chat.twitch.tv", "#" + str(channel)))
        personality_thread = threading.Thread(target=self.analyze_personality, args=(personality_analyzer,))
        language_thread = threading.Thread(target=self.analyze_language, args=(language_analyzer,))

        tone_analyzer_thread.daemon = True
        jeffy_thread.daemon = True
        personality_thread.daemon = True
        language_thread.daemon = True

        jeffy_thread.start()
        tone_analyzer_thread.start()
        personality_thread.start()
        language_thread.start()

    def get_user_stats(self):
        """
        Web interface that returns stats on a user's toxicity and total number of messages
        :return: dictionary of stats on a user's toxicity and total number of messages
        """
        profDict = {}
        for key in self.profiles:
            prof = self.profiles[key]
            toxicity = prof.toxicity
            if toxicity is None:
                toxicity = 0
            profInfo = {"name": prof.username, "toxicity": toxicity, "size": prof.numMessages}
            profDict[prof.username] = profInfo
        return profDict

    def analyze_language(self, analyzer):
        """
        takes in a message, determines the language that it is in, and translates it if necessary
        :param analyzer: instantiation of the language analyzer class, used to analyze the language and translate to
                            english if possible
        :return: None
        """
        while True:
            while not self.toBeTranslated.empty():
                message = self.toBeTranslated.get()
                name = message[0]
                message = analyzer.translate_message(message[1])
                self.messages.put((name, message))
            time.sleep(1)

def main(channel):
    """
    creates and runs an instance of ToxBot
    :return: None
    """
    tox_bot = ToxBot()
    intrfce = JeffyWebInterface(80,tox_bot)
    intrfce.startRESTinterface()
    tox_bot.run(channel)
    
    input()
    intrfce.stopRESTinterface()

if __name__ == '__main__':
    main(sys.argv[1])
