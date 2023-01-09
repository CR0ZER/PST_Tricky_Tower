import time
import logging
import logging.handlers
import base64

# twisted
from twisted.internet.protocol import Factory
from twisted.internet import reactor
from twisted.protocols.basic import LineReceiver

from gamelogic import *
from datahandler import *
import global_vars as g

dataHandler = None


def startServer():
    # start gui
    # serverGUI = ServerGUI()

    # start logging
    setupLogging()

    # start server
    global dataHandler

    startTime = time.time()

    g.serverLogger.info("Starting server...")

    factory = gameServerFactory()
    reactor.listenTCP(2727, factory)
    g.conn = factory.protocol(factory)

    loadGameData()

    dataHandler = DataHandler()

    endTime = time.time()
    totalTime = (endTime - startTime)*1000
    g.serverLogger.info(
        "Initialization complete. Server loaded in " + str(round(totalTime, 2)) + " ms.")

    # start the server loop and the reactor
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
        global dataHandler
        clientIndex = self.factory.clients.index(self)

        g.connectionLogger.debug(
            "Received data from " + str(self.transport.getPeer().host))
        g.connectionLogger.debug(" -> " + str(data))

        dataHandler.handleData(clientIndex, data)

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
clockTick = 0
tmr500 = 0
tmr1000 = 0
lastUpdatePlayerVitals = 0
lastUpdateMapSpawnItems = 0
lastUpdateSavePlayers = 0
lastRegenNpcHp = 0


def serverLoop():
    global clockTick, tmr500, tmr1000, lastUpdatePlayerVitals, lastUpdateSavePlayers, lastUpdateMapSpawnItems

    clockTick = time.time() * 1000

    if clockTick > tmr1000:
        # handle shutting down server

        # handle closing doors

        tmr1000 = time.time() * 1000 + 1000

    # loop the serverLoop function every half second
    reactor.callLater(0.5, serverLoop)
