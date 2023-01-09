
from twisted.internet import protocol, reactor
import pygame
from constants import *
from network import *
import engine
import global_vars as g

from utils import *


def main():
    pygame.init()
    # start game
    g.gameEngine = engine.Engine()
    log("start init")
    g.gameEngine.init()


# this only runs if the module was *not* imported
if __name__ == "__main__":
    main()
