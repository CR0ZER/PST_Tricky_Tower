from twisted.internet.protocol import Protocol, Factory, ClientFactory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor, error
from twisted.python.failure import Failure

from constants import *
from datahandler import *


def startConnection():
    global dataHandler
    factory = gameClientFactory()
    g.connector = reactor.connectTCP(GAME_IP, GAME_PORT, factory)
    dataHandler = DataHandler()

    return factory.protocol


class gameClientProtocol(LineReceiver):
    MAX_LENGTH = (
        999999  # todo: find a suitable size (see client: sendMap (in clienttcp.py))
    )

    def __init__(self, factory):
        self.factory = factory

    def connectionMade(self):
        """called when connection has been made"""
        """ used for logging in and new account """

        # if g.gameState == MENU_LOGIN:
        #    # logging in, so send login after connection has been established
        #    username = g.gameEngine.menuLogin.username
        #    password = g.gameEngine.menuLogin.password

        #    g.tcpConn.sendLogin(username, password)

        # log("Connection established to server")

    def lineReceived(self, data):
        global dataHandler

        # handle base64 data
        decodedData = str(data)
        # log("Received data from server")
        # log(" -> " + decodedData)

        dataHandler.handleData(decodedData)

    def sendData(self, data):
        # encode data using base64
        encodedData = bytearray(data, "utf-8")
        self.sendLine(encodedData)


class gameClientFactory(ClientFactory):
    def __init__(self):
        self.protocol = gameClientProtocol(self)

    def startedConnecting(self, connector):

        print("Connecting to server...")

    def buildProtocol(self, addr):
        return self.protocol

    def clientConnectionFailed(self, connector, reason):
        # errorMsg = reason.getErrorMessage().split(':')
        # alertMessageDialog('Unable to connect to server: ' + errorMsg[1] + errorMsg[2], 'An error occured')
        print(reason.getErrorMessage())

    def clientConnectionLost(self, connector, reason):
        print(reason.getErrorMessage())
        try:
            ##reactor.stop()
            print("Disconnection from server")
        except error.ReactorNotRunning:
            pass
