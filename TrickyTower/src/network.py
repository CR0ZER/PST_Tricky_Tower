from twisted.internet.protocol import Protocol, Factory, ClientFactory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor, error
from twisted.python.failure import Failure

import base64

from constants import *
from datahandler import *
import global_vars as g
from utils import *


def startConnection():
    global dataHandler
    factory = gameClientFactory()
    g.connector = reactor.connectTCP(GAME_IP, GAME_PORT, factory)
    dataHandler = DataHandler()

    return factory.protocol


class gameClientProtocol(LineReceiver):
    MAX_LENGTH = (
        # todo: find a suitable size (see client: sendMap (in clienttcp.py))
        999999
    )

    def __init__(self, factory):
        self.factory = factory

    def connectionMade(self):
        """called when connection has been made"""
        """ used for logging in and new account """

        if g.gameState == MENU_LOGIN:
            # logging in, so send login after connection has been established
            username = "bob"  # g.gameEngine.menuLogin.username
            password = "password"  # g.gameEngine.menuLogin.password

            g.tcpConn.sendLogin(username, password)
            log("Connection established to server")

    def lineReceived(self, data):
        global dataHandler

        # log("Received data from server")
        # log(" -> " + str(data))

        dataHandler.handleData(data)

    def sendData(self, data):
        # encode data using base64
        # encodedData = base64.b64encode(data)
        encodedData = bytes(data, "utf-8")
        self.sendLine(encodedData)


class gameClientFactory(ClientFactory):
    def __init__(self):
        self.protocol = gameClientProtocol(self)

    def startedConnecting(self, connector):

        log("Connecting to server...")

    def buildProtocol(self, addr):
        return self.protocol

    def clientConnectionFailed(self, connector, reason):
        # errorMsg = reason.getErrorMessage().split(':')
        # alertMessageDialog('Unable to connect to server: ' + errorMsg[1] + errorMsg[2], 'An error occured')
        log(reason.getErrorMessage())

    def clientConnectionLost(self, connector, reason):
        log(reason.getErrorMessage())
        try:
            # reactor.stop()
            log("Disconnection from server")
        except error.ReactorNotRunning:
            pass


class TCPConnection:
    def __init__(self, protocol):
        self.protocol = protocol

    def sendData(self, data):
        self.protocol.sendData(data)

    def sendLogin(self, username, password):
        packet = json.dumps(
            [{"packet": ClientPackets.CLogin, "name": username, "password": password}],
            ensure_ascii=False,
        )
        self.sendData(packet)

    def sendQuit(self):
        packet = json.dumps([{"packet": ClientPackets.CQuit}])
        self.sendData(packet)
