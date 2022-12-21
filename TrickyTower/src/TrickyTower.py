# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.


"""
An example client. Run simpleserv.py first before running this.
"""

from twisted.internet import protocol, reactor
import time
import pygame
from constants import *
from network import *

# a client protocol
def log(msg):
    """Prints @msg to the terminal with a timestamp"""
    localTime = time.localtime(time.time())
    stringTime = str(localTime[3]) + ":" + str(localTime[4]) + ":" + str(localTime[5])

    print(stringTime + ": " + msg)


# this connects the protocol to a server running on port 8000
def main():
    pygame.init()
    f = EchoFactory()
    reactor.connectTCP("localhost", 8000, f)
    reactor.run()


# this only runs if the module was *not* imported
if __name__ == "__main__":
    main()
