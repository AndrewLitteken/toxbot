#!/usr/bin/env python3

import queue, heapq, threading
from ircbot import IRCbot
from ToneAnalyzer import ToneAnalyzer
from PersonalityAnalyzer import PersonalityAnalyzer
import time


class ToxBot:
    def __init__(self):
        self.messages = queue.Queue()
        self.personalityQueue = queue.Queue()
        self.profiles = {}
        self.whitelist = {}
        self.threshold = -.6
        self.toxicity = 0

    class Profile:
        def __init__(self, usr, message):
            self.username = usr
            self.numMessages = 1
            self.bad = []
            heapq.heappush(self.bad, (message[1], message))
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
            while len(self.bad) > 10:  # only keeps the worst 10 messages
                del self.bad[10]
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
            new_tox = personalityAnalyzer.analyze_personality(self.recent)
            self.recent.clear()
            self.inQueue = False
            if self.toxicity is None:  # if there have been no prior analyses, toxicity is based on this analysis only
                self.toxicity = new_tox
            else:  # if there have been prior analyses, then add this to total analysis as an average
                scale = num_new_messages / self.numMessages
                self.toxicity = self.toxicity * scale + new_tox * (1 - scale)

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
                    if message[0] in self.profiles:  # if the profile exists, add the message to the profile
                        profile_message = (message[1], score)
                        self.profiles[message[0]].add_message(profile_message, self.personalityQueue)
                    else:  # if the profile does not exist, create a profile with this message as the first
                        if score < self.threshold:
                            print("\t\t\t" + str(message))

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
        jeffy = IRCbot(usr, auth, irc, channel, self.messages)
        jeffy.listen()

    def get_profiles(self):
        """
        creates and returns a dictionary of profiles for the web application
        :return: dictionary of users to their worst 10 messages and their overall toxicity
        """
        profDict = {}
        for key in self.profiles:
            prof = self.profiles[key]
            bad = []
            for item in prof.bad:
                bad.append(list(item[1]))
            toxicity = prof.toxicity
            if toxicity is None:
                toxicity = 0
            profInfo = {"username": prof.username, "worst_messages": bad, "toxicity": toxicity}
            profDict[prof.username] = profInfo
        return profDict

    def run(self):
        """
        Creates the instantiations of the analyzer classes, creates and starts the threads
        :return: None
        """
        toneAnalyzer1 = ToneAnalyzer('a54c1a30-92fe-4c1f-b34a-02936047e396', '8WTlVVDHFHCt', '2016-05-19',
                                     "./data/text", "./data/scores", False)
        personalityAnalyzer1 = PersonalityAnalyzer('023391c6-0462-4720-8db4-42d03a32a89a', '6arBBasLMdQQ', '2016-9-20')

        # toneAnalyzer2 = ToneAnalyzer('a54c1a30-92fe-4c1f-b34a-02936047e396', '8WTlVVDHFHCt', '2016-05-19');
        # thread.start_new_thread(analyze_tone, (analyzer2, messages));

        toneAnalyzerThread = threading.Thread(target=self.analyze_tone, args=(toneAnalyzer1,))
        jeffyThread = threading.Thread(target=self.jeffy_listen,
                                       args=("johnathonnow", "oauth:mm84kpr5or9rmashwlp9f8dxprqm3b", "irc.chat.twitch.tv", "#summit1g"))
        personalityThread = threading.Thread(target=self.analyze_personality, args=(personalityAnalyzer1,))

        toneAnalyzerThread.daemon = True
        jeffyThread.daemon = True
        personalityThread.daemon = True

        jeffyThread.start()
        toneAnalyzerThread.start()
        personalityThread.start()


def main():
    """
    creats and runs an instance of ToxBot
    :return: None
    """
    toxBot = ToxBot()
    toxBot.run()
    while True:
        pass


if __name__ == '__main__':
    main()
