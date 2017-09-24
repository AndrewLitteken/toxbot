#! /usr/bin/env python3

from WebInterfaces.JeffyWebInterface import JeffyWebInterface
import ToxBot

# tox_bot = None
tox_bot = ToxBot()
tox_bot.run()

intrfce = JeffyWebInterface(8080,tox_bot)
intrfce.startRESTinterface()

input()
intrfce.stopRESTinterface()
