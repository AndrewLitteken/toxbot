#!/usr/bin/env python3

import socket


class IRCbot(object):
    def __init__(self, user, passw, server, channel, q):
        self.irc = IRC()
        self.user = user
        self.passw = passw
        self.channel = channel
        self.irc.connect(server, channel, user, passw)
        self.q = q

    def on_chat(self, who, msg):
        """
        When a chat has occurred, push it to the processing queue
        :param who: username of chat user
        :param msg: their chat message
        :return: places value into the chat queue
        """
        if who != self.user:
            self.q.put((str(who), str(msg)))
            # print("{}: {}".format(str(who), msg))

    def listen(self):
        """
        Listens to the IRC channel for messages
        :return: None
        """

        buf = ""
        while True:
            buf += self.irc.receive()
            n_buf = ""
            for buff in buf.split("\r\n"):
                if len(buff) > 0 and buff[0] == ':' and 'PRIVMSG' in buff:
                    # A message has been sent
                    who = buff[1:].split('!')[0].strip()
                    self.channel = buff.split('PRIVMSG', 1)[1].split(':', 1)[0].strip()
                    message = buff.split('PRIVMSG', 1)[1].split(':', 1)[1].strip()
                    self.on_chat(who, message)
                n_buf = buff
            buf = n_buf

    def do_to_user(self, action, user):
        """
        Performs /action on user using the twitch chat commands
        :param action: what action to do
        :param user: what user to do something to
        :return: None
        """
        self.irc.send(self.channel, '/{} {}'.format(action, user))

    def send(self, message):
        """
        Sends a message to the current IRC channel
        :param message: what is to be sent
        :return: None
        """
        self.irc.send(self.channel, message)

    def send_image(self, image_url, message=''):
        """
        Sends an image (and message) to the current IRC channel
        :param image_url: path to image to send
        :param message: what is to be sent
        :return:
        """
        self.send(message + image_url)


class IRC:
    irc = socket.socket()
  
    def __init__(self):
        self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
    def quit(self):
        """
        Quits the current IRC channel
        :return:
        """
        self.irc.send(bytes("QUIT " + " :kbye...\r\n", encoding="utf-8"))

    def send(self, channel, msg):
        """
        Sends a message to the channel
        :param channel: which channel to send to
        :param msg: message to send
        :return: None
        """
        self.irc.send(bytes("PRIVMSG " + channel + " :" + msg + "\r\n", encoding="utf-8"))
 
    def connect(self, server, channel, nick, password):
        """
        Joins a channel within a server.
        :param server: name of server to join
        :param channel: name of channel to join
        :param nick: name of usr
        :param password: password for usr
        :return:
        """
        # TODO: error check all this
        self.irc.connect((server, 6667))
        self.irc.send(bytes("PASS " + password + "\r\n", encoding="utf-8"))
        self.irc.send(bytes("NICK " + nick + "\r\n", encoding="utf-8"))
        self.irc.send(bytes("JOIN " + channel + "\r\n", encoding="utf-8"))
 
    def pong(self, buff):
        """
        Required for IRC chatting
        :param buff: buffer received from IRC to process and pong back
        :return:
        """
        if buff.find('PING') != -1:
            self.irc.send(bytes('PONG ' + buff.split()[1] + '\r\n', encoding="utf-8"))

    def receive(self):
        buff = self.irc.recv(2040).decode("utf-8") 
        self.pong(buff)
        return buff
