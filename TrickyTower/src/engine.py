import time
import pygame
from pygame.locals import *

from twisted.internet import reactor

from network import *
from constants import *
import global_vars as g


class Engine:
    def __init__(self):
        self.FRAMES_PER_SECOND = 20

        # menus

        self.tmr25 = 0
        self.tmr1000 = 0
        self.walkTimer = 0
        self.clockTick = 0

    def init(self):

        # self.initConfig(g.dataPath + '/config.cfg')
        g.gameEngine.initConnection()

        self.gameLoop()
        reactor.run()

    def initConnection(self):
        """starts the connection to the server"""
        connectionProtocol = startConnection()
        g.tcpConn = TCPConnection(connectionProtocol)

    def initConfig(self, configFile):
        """reads the configuration file"""
        log("can read config.cfg file here")

    def disconnect(self):
        g.connector.disconnect()

    def setState(self, state):
        """sets the game state"""
        if state == MENU_LOGIN:
            g.gameState = MENU_LOGIN

        elif state == MENU_REGISTER:
            g.gameState = MENU_REGISTER

        elif state == MENU_CHAR:
            g.gameState = MENU_CHAR

        elif state == MENU_NEWCHAR:
            g.gameState = MENU_NEWCHAR

        elif state == MENU_INGAME:
            g.gameState = MENU_INGAME

    def gameLoop(self, FPS=25):
        """the main loop of the game"""
        # TODO: DIRTY AREAS
        if g.gameState == MENU_LOGIN:
            pass

        elif g.gameState == MENU_REGISTER:
            pass

        elif g.gameState == MENU_CHAR:
            pass

        elif g.gameState == MENU_NEWCHAR:
            pass

        elif g.gameState == MENU_INGAME:
            # todo: dirty areas

            # self.graphicsEngine.renderGraphics()

            # flip graphics
            pygame.display.update()
            # pygame.display.update(self.graphicsEngine.dirtyRects)

        # pygame.event.pump()
        # for event in pygame.event.get():
        #    # todo: organize this better...
        #    if g.gameState == MENU_LOGIN:
        #        pass
        #
        #    elif g.gameState == MENU_REGISTER:
        #        pass
        #
        #    elif g.gameState == MENU_CHAR:
        #        pass
        #
        #    elif g.gameState == MENU_NEWCHAR:
        #        pass
        #    elif g.gameState == MENU_INGAME:
        #        pass
        #
        #    if event.type == pygame.QUIT:
        #        reactor.stop()
        #        pygame.quit()
        #
        #    elif event.type == pygame.MOUSEMOTION:
        #        self.handleMouse(event)

        # make it loop
        reactor.callLater(1.0 / FPS, self.gameLoop)

    def quitGame(self):
        """called when quitting the game"""
        if g.tcpConn != None:
            # if connected to server, send quit msg
            g.tcpConn.sendQuit()

        reactor.stop()
        pygame.quit()

    ##################
    # INPUT SPECIFIC #
    #################

    def checkInputKeys(self):
        """checks for input events"""

        def pressed(key):
            keys = pygame.key.get_pressed()

            if keys[key]:
                return True
            else:
                return False

        if pressed(pygame.K_UP) or pressed(pygame.K_z):
            g.inpDIR_UP = True
            g.inpDIR_DOWN = False
            g.inpDIR_LEFT = False
            g.inpDIR_RIGHT = False

        elif pressed(pygame.K_DOWN) or pressed(pygame.K_s):
            g.inpDIR_UP = False
            g.inpDIR_DOWN = True
            g.inpDIR_LEFT = False
            g.inpDIR_RIGHT = False

        elif pressed(pygame.K_LEFT) or pressed(pygame.K_q):
            g.inpDIR_UP = False
            g.inpDIR_DOWN = False
            g.inpDIR_LEFT = True
            g.inpDIR_RIGHT = False

        elif pressed(pygame.K_RIGHT) or pressed(pygame.K_d):
            g.inpDIR_UP = False
            g.inpDIR_DOWN = False
            g.inpDIR_LEFT = False
            g.inpDIR_RIGHT = True

        else:
            g.inpDIR_UP = False
            g.inpDIR_DOWN = False
            g.inpDIR_LEFT = False
            g.inpDIR_RIGHT = False
            g.inpSHIFT = False
            g.inpCTRL = False

    def handleMouse(self, event):
        g.cursorX = event.pos[0]
        g.cursorY = event.pos[1]

        # only set mouse tile position within game screen boundaries
        # if g.cursorX > 16 and g.cursorX < (16 + 15 * PIC_X):
        # g.cursorXTile = (g.cursorX - 16) // PIC_X
        ##
        # if g.cursorY > 16 and g.cursorY < (16 + 11 * PIC_Y):
        # g.cursorYTile = (g.cursorY - 16) // PIC_Y
