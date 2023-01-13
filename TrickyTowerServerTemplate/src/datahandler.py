from constants import *
from packettypes import *
from gamelogic import *
from utils import *

import global_vars as g

import json


class DataHandler():
    def handleData(self, index, data):
        if data:
            # log(str(data))
            jsonData = json.loads(data)
            packetType = jsonData[0]["packet"]

            if packetType == ClientPackets.CQuit:
                self.handleQuit(index)
            elif packetType == ClientPackets.CArrowKey:
                self.handleKey(index, jsonData)
            elif packetType == ClientPackets.CNewPlayer:
                self.handleNewPlayer()

            else:
                # Packet is unknown - hacking attempt
                log(str(index) + 'Packet Modification')

    ''' Player login '''

    def handleNewPlayer(self):
        g.game.nbplayer += 1

    def handleQuit(self, index):
        closeConnection(index)

    def handleKey(self, index, jsonData):
        g.game.players[index].key[jsonData[0]["key"]] = jsonData[0]["actived"]
