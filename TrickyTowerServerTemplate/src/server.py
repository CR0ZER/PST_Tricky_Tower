import pygame
import time
import logging
import logging.handlers
import pymunk

import pymunk.pygame_util
# twisted
from twisted.internet.protocol import Factory
from twisted.internet import reactor
from twisted.protocols.basic import LineReceiver

from gamelogic import *
from datahandler import *
import global_vars as g
from objects import *


def startServer():
    # start gui
    # serverGUI = ServerGUI()

    # start logging
    setupLogging()

    # start server

    startTime = time.time()

    g.serverLogger.info("Starting server...")

    factory = gameServerFactory()
    reactor.listenTCP(2727, factory)
    g.conn = factory.protocol(factory)

    loadGameData()

    g.dataHandler = DataHandler()

    endTime = time.time()
    totalTime = (endTime - startTime)*1000
    g.serverLogger.info(
        "Initialization complete. Server loaded in " + str(round(totalTime, 2)) + " ms.")

    # start the server loop and the reactor
    g.game = Game()
    g.game.launch()

    serverLoop()
    reactor.run()


def setupLogging():
    ''' setup loggers for server (general) and connection (in/out) '''
    ''' max log size is 1mb '''
    # stream handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(logging.Formatter(
        '%(asctime)s (%(name)s) %(levelname)s: %(message)s'))

    # file handler
    fh = logging.handlers.RotatingFileHandler(
        filename='../server.log', maxBytes=1048576, backupCount=5)
    fh.setLevel(logging.INFO)
    fh.setFormatter(logging.Formatter(
        '%(asctime)s (%(name)s) %(levelname)s: %(message)s'))

    g.serverLogger = logging.getLogger('server')
    g.serverLogger.setLevel(logging.INFO)
    g.serverLogger.addHandler(ch)
    g.serverLogger.addHandler(fh)

    g.connectionLogger = logging.getLogger('connection')
    g.connectionLogger.setLevel(logging.INFO)
    g.connectionLogger.addHandler(ch)
    g.connectionLogger.addHandler(fh)


def loadGameData():
    pass


class gameServerProtocol(LineReceiver):
    # todo: find a suitable size (see client: sendMap (in clienttcp.py))
    MAX_LENGTH = 999999

    def __init__(self, factory):
        self.factory = factory

    def connectionMade(self):
        self.factory.clients.append(self)
        g.connectionLogger.info(
            "CONNECTION - Connection from IP: " + str(self.transport.getPeer().host))

    def connectionLost(self, reason):
        clientIndex = self.factory.clients.index(self)
        self.transport.loseConnection()
        closeConnection(clientIndex)

        self.factory.clients.remove(self)

    def lineReceived(self, data):
        clientIndex = self.factory.clients.index(self)

        g.connectionLogger.debug(
            "Received data from " + str(self.transport.getPeer().host))
        g.connectionLogger.debug(" -> " + str(data))

        g.dataHandler.handleData(clientIndex, data)

    def closeConnection(self, index):
        ''' closes connection with client #index '''
        log('closeConnection()')

    def sendDataTo(self, index, data):
        # encode data using base64
        # encodedData = base64.b64encode(data)
        encodedData = bytes(data, "utf-8")
        self.factory.clients[index].sendLine(encodedData)

    def sendDataToAll(self, data):
        for i in range(0, len(self.factory.clients)):
            self.sendDataTo(i, data)

    def sendDataToAllBut(self, index, data):
        for i in range(0, len(self.factory.clients)):
            if i == index:
                continue
            else:
                self.sendDataTo(i, data)


class gameServerFactory(Factory):
    protocol = gameServerProtocol

    def __init__(self):
        self.clients = []

    def buildProtocol(self, addr):
        p = self.protocol(self)
        p.factory = self
        return p


# server loop and timings
pygame.init()
screen = pygame.display.set_mode((1080, 720))
print_options = pymunk.pygame_util.DrawOptions(screen)
# print_options = pymunk.SpaceDebugDrawOptions()  # For easy printing
# print_options.flags = pymunk.SpaceDebugDrawOptions.DRAW_SHAPES

enablePh = True


def serverLoop():
    global enablePh
    g.clockTime = time.time()

    if enablePh == True:
        g.game.space.step(0.02)
        g.game.removeFalledBlocks()
        for i in range(4):
            g.game.playerInput(i)
            g.game.playerMove(i)
            g.game.checkPlayerCollide(i)

    screen.fill(pygame.Color("black"))
    g.game.space.debug_draw(print_options)
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                enablePh = not (enablePh)

    sendBlock()  # Envoie tout les blocks aux clients

    t = time.time() - g.clockTime
    # log("tts :" + str(t))
    if (t > 0.02):
        reactor.callLater(0.001, serverLoop)
    else:
        reactor.callLater(0.02 - t, serverLoop)
