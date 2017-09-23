#! /usr/bin/env python3

from WebInterfaces.JeffyWebInterface import JeffyWebInterface

test = JeffyWebInterface(8080,None)
test.startRESTinterface()

input()
test.stopRESTinterface()
