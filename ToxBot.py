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
            self.recent.append(message)
            heapq.heappush(self.bad, (message[1], message))
            while len(self.bad) > 10:
                del self.bad[10]
            self.numMessages += 1
            if len(self.recent) >= 3 and not self.inQueue:
                personalityQueue.put(self)
                self.inQueue = True

        def update_personality(self, personalityAnalyzer):
            num_new_messages = len(self.recent)
            new_tox = personalityAnalyzer.analyze_personality(self.recent)
            print("~~~~~~~~~~~~~~Toxiscity level:" + str(new_tox))
            self.recent.clear()
            self.inQueue = False
            if self.toxicity is None:
                self.toxicity = new_tox
            else:
                scale = num_new_messages / self.numMessages
                self.toxicity = self.toxicity * scale + new_tox * (1 - scale)

    def analyze_tone(self, analyzer):
        while True:
            while not self.messages.empty():
                message = self.messages.get()
                score = analyzer.get_score(message[1])
                if message[0] in self.profiles:
                    profile_message = (message[1], score)
                    self.profiles[message[0]].add_message(profile_message, self.personalityQueue)
                else:
                    if score < self.threshold:
                        print("\t\t\t" + str(message))

                    profile_message = (message[1], score)
                    self.profiles[message[0]] = self.Profile(message[0], profile_message)
            time.sleep(2)

    def analyze_personality(self, analyzer):
        while True:
            while not self.personalityQueue.empty():
                print("!!!!!!!!!!GETTING PERSONALITY!!!!!!!!!!")
                profile = self.personalityQueue.get()
                profile.update_personality(analyzer)
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
        print('hello run')
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
    toxBot = ToxBot()
    toxBot.run()
    while True:
        pass


if __name__ == '__main__':
    main()
