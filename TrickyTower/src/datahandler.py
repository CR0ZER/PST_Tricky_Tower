from constants import *
import global_vars as g
from packettypes import *
import json
from pymunk.vec2d import *

from utils import *


class DataHandler:
    """class for handling data sent from the server"""

    def __init__(self, protocol=2):
        self.protocol = protocol

    def handleData(self, data):
        jsonData = json.loads(data)
        packetType = jsonData[0]["packet"]

        if packetType == ServerPackets.SLoginOK:
            self.handleSLoginOK(jsonData)
        elif packetType == ServerPackets.SSendBlock:
            self.handleBlock(jsonData)
        elif packetType == ServerPackets.SBeginBlock:
            self.handleBeginPacket()
        elif packetType == ServerPackets.SEndBlock:
            self.handleEndPacket()
        elif packetType == ServerPackets.SPlayerCount:
            self.handlePlayerCount(jsonData)
        elif packetType == ServerPackets.SGameStart:
            self.handleGameStart()
        elif packetType == ServerPackets.SWinner:
            self.handleWinner(jsonData)
        else:
            # Packet is unknown - hacking attempt
            # log("potential hacking attempt")
            pass

    def handleBlock(self, jsonData):
        g.NewBlock.append((Vec2d(jsonData[0]["positionX"], jsonData[0]["positionY"]), Vec2d(
            jsonData[0]["rotationX"], jsonData[0]["rotationY"]), jsonData[0]["type"]))
        #log(f"Type : {g.NewBlock[0][2]} \n")
        # log("position" + str(jsonData[0]["positionY"]))

    def handleAlertMsg(self, jsonData):
        msg = jsonData[0]["msg"]

        log(msg)

    def handleBeginPacket(self):
        g.NewBlock.clear()

    def handleEndPacket(self):
        g.Blocks.clear()
        g.Blocks = g.NewBlock.copy()

    def handlePlayerCount(self, jsonData):
        g.nbPlayers = jsonData[0]["nbPlayers"]

    def handleGameStart(self):
        g.gameState = 1

    def handleWinner(jsonData):
        g.winner = jsonData[0]["winner"]
        g.gameState = 2