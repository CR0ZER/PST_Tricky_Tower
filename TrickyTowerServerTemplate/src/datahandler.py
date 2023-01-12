from constants import *
from packettypes import *
from gamelogic import *
from utils import *

import global_vars as g

import json


class DataHandler():
    def handleData(self, index, data):
        if data:
            log(str(data))
            jsonData = json.loads(data)
            packetType = jsonData[0]["packet"]

            if packetType == ClientPackets.CLogin:
                self.handleLogin(index, jsonData)

            elif packetType == ClientPackets.CQuit:
                self.handleQuit(index)
            elif packetType == ClientPackets.CArrowKey:
                self.handleKey(index, jsonData)

            else:
                # Packet is unknown - hacking attempt
                log(str(index) + 'Packet Modification')

    ''' Player login '''

    def handleLogin(self, index, jsonData):
        if not isLoggedIn(index):

            plrName = jsonData[0]["name"]
            plrPassword = jsonData[0]["password"]

            # todo: check version

            if len(plrName) < 3 or len(plrPassword) < 3:
                alertMsg(index, "The acount name or password is too short!")
                return

            if isMultiAccounts(plrName):
                alertMsg(index, "That account is already logged in!")
                g.conn.closeConnection(index)

                return

            g.connectionLogger.info(str(index) + ' has logged in')

    def handleQuit(self, index):
        closeConnection(index)

    def handleArrow(self, index, jsonData):
        g.game.players[index].key = jsonData[0]["key"]
