from turtle import Vec2D
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

        else:
            # Packet is unknown - hacking attempt
            log("potential hacking attempt")

    def handleBlock(self, jsonData):
        g.Blocks.append((Vec2d(jsonData[0]["positionX"], jsonData[0]["positionY"]), Vec2d(
            jsonData[0]["rotationX"], jsonData[0]["rotationY"])))
        log("position" + str(jsonData[0]["positionY"]))

    def handleAlertMsg(self, jsonData):
        msg = jsonData[0]["msg"]

        log(msg)
