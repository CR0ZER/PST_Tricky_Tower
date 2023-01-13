
import json

from constants import *
from packettypes import *
from utils import *
from objects import *

import global_vars as g


def joinGame(index):

    # send ok to client to start receiving game data
    packet = json.dumps([{"packet": ServerPackets.SLoginOK, "index": index}])
    g.conn.sendDataTo(index, packet)

    # send that we're ingame
    packet = json.dumps([{"packet": ServerPackets.SInGame}])
    g.conn.sendDataTo(index, packet)


def leftGame(index):
    log("la biz : " + str(index) + ".")


def closeConnection(index):
    if index >= 0:
        leftGame(index)

        g.connectionLogger.info("Connection from " +
                                str(index) + " has been terminated.")


def sendBlock():
    packet = json.dumps([{"packet": ServerPackets.SBeginBlock}])
    g.conn.sendDataToAll(packet)
    for i in range(g.game.nbplayer):
        bp = g.game.players[i].block
        packet = json.dumps([{"packet": ServerPackets.SSendBlock, "positionX": bp.body._get_position().x, "positionY": bp.body._get_position().y, "rotationX": bp.body._get_rotation_vector().x,
                            "rotationY": bp.body._get_rotation_vector().y, "type": bp.type}])
        g.conn.sendDataToAll(packet)
    for b in g.game.blocks + g.game.static_Blocks:
        packet = json.dumps([{"packet": ServerPackets.SSendBlock, "positionX": b.body._get_position().x, "positionY": b.body._get_position().y, "rotationX": b.body._get_rotation_vector().x,
                            "rotationY": b.body._get_rotation_vector().y, "type": b.type}])
        g.conn.sendDataToAll(packet)
    packet = json.dumps([{"packet": ServerPackets.SEndBlock}])
    g.conn.sendDataToAll(packet)


def sendPlayerCount():
    packet = json.dumps(
        [{"packet": ServerPackets.SPlayerCount, "number": g.game.nbplayer}])
    g.conn.sendDataToAll(packet)


def sendGameStart():
    packet = json.dumps(
        [{"packet": ServerPackets.SGameStart}])
    g.conn.sendDataToAll(packet)


def sendWinner(index):
    if index:
        packet = json.dumps(
            [{"packet": ServerPackets.SWinner, "player": index}])
        g.conn.sendDataToAll(packet)
