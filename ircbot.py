#!/usr/bin/env python3
import socket
import queue
import sys

class IRCbot(object):
    def __init__(self, user, passw, server, channel, q):
        self.irc = IRC()
        self.user = user
        self.passw = passw
        self.channel = None
        self.irc.connect(server, channel, user, passw)
        self.q = q

    def on_chat(self, who, msg, buf):
        if who != self.user:
            self.q.put((str(who), str(msg)))
            # print("{}: {}".format(str(who), msg))

    def listen(self):
        buf = ""
        while True:
             buf += self.irc.recieve()
             nbuf = ""
             for buff in buf.split("\r\n"):
                 if len(buff) > 0 and buff[0] == ':' and 'PRIVMSG' in buff:
                     #it is a message
                     who = buff[1:].split('!')[0].strip()
                     self.channel = buff.split('PRIVMSG', 1)[1].split(':', 1)[0].strip()
                     message = buff.split('PRIVMSG', 1)[1].split(':', 1)[1].strip()
                     self.on_chat(who, message, buff)
                 nbuf = buff
             buf = nbuf



    def send(self, message):
        self.irc.send(self.channel, message)

    def sendImage(self, image_url, message = ''):
        self.send(message + image_url)
 
class IRC:
    irc = socket.socket()
  
    def __init__(self):  
        self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
    def quit(self, channel, debug=False):
        self.irc.send(bytes("QUIT " + " :kbye...\r\n", encoding="utf-8"))

    def send(self, channel, msg, debug=False):
        self.irc.send(bytes("PRIVMSG " + channel + " :" + msg + "\r\n", encoding="utf-8"))
 
    def connect(self, server, channel, nick, password, debug=False):
        # TODO: error check all this
        self.irc.connect((server, 6667))
        self.irc.send(bytes("PASS " + password + "\r\n", encoding="utf-8"))
        self.irc.send(bytes("NICK " + nick + "\r\n", encoding="utf-8"))
        #self.irc.send("USER " + nick + " " + server + nick + " : " + nick + "\r\n") 
        self.irc.send(bytes("JOIN " + channel + "\r\n", encoding="utf-8"))
 
    def pong(self, buff, debug=False):
        if buff.find('PING') != -1:
            self.irc.send(bytes('PONG ' + buff.split()[1] + '\r\n', encoding="utf-8"))

    def recieve(self, debug=False):
        buff = self.irc.recv(2040).decode("utf-8") 
        self.pong(buff, debug)
        return buff

#q = queue.Queue()
#jeffy = IRCbot("johnathonnow", "oauth:mm84kpr5or9rmashwlp9f8dxprqm3b", "irc.chat.twitch.tv", "#summit1g", q)
#jeffy.listen()
