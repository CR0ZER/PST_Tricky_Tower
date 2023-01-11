
import json

from constants import *
from packettypes import *
from utils import *
from objects import *

import global_vars as g


def joinGame(index):
    TempPlayer[index].inGame = True

    g.totalPlayersOnline += 1

    globalMsg(index + " has joined!", textColor.WHITE)

    # send ok to client to start receiving game data
    packet = json.dumps([{"packet": ServerPackets.SLoginOK, "index": index}])
    g.conn.sendDataTo(index, packet)

    # send that we're ingame
    packet = json.dumps([{"packet": ServerPackets.SInGame}])
    g.conn.sendDataTo(index, packet)


def leftGame(index):
    log("tkt : " + str(index) + ".")
    if TempPlayer[index].inGame:
        TempPlayer[index].inGame = False

        # send global msg that player left game
        globalMsg(index + ' has left ' + GAME_NAME + '!', textColor.WHITE)

        g.connectionLogger.info(index + ' has disconnected')
        sendLeftGame(index)

        g.totalPlayersOnline -= 1

# (SHOULD BE IN SERVER.TCP?)
####################
# SERVER FUNCTIONS #
####################


def globalMsg(msg, color=(255, 0, 0)):
    packet = json.dumps(
        [{"packet": ServerPackets.SGlobalMsg, "msg": msg, "color": color}])
    g.conn.sendDataToAll(packet)


def playerMsg(index, msg, color=(255, 0, 0)):
    packet = json.dumps(
        [{"packet": ServerPackets.SPlayerMsg, "msg": msg, "color": color}])
    g.conn.sendDataTo(index, packet)


def alertMsg(index, reason):
    packet = json.dumps([{"packet": ServerPackets.SAlertMsg, "msg": reason}])
    g.conn.sendDataTo(index, packet)


def isLoggedIn(index):
    if len(Player[index].Login) > 0:
        return True


def isMultiAccounts(login):
    for i in range(g.totalPlayersOnline):
        if str(Player[g.playersOnline[i]].Login).lower() == login.lower():
            return True

    return False


def closeConnection(index):
    if index >= 0:
        leftGame(index)

        g.connectionLogger.info("Connection from " +
                                str(index) + " has been terminated.")


def sendWhosOnline(index):
    msg = ''
    n = 0

    for i in range(g.totalPlayersOnline):
        if g.playersOnline[i] != index:
            n += 1

    if n == 0:
        msg = 'There are no other players online.'
    else:
        msg = 'There are ' + str(n) + ' other players online.'

    playerMsg(index, msg, whoColor)


def sendLeftGame(index):
    # TODO Make name non or smth
    packet = json.dumps([{"packet": ServerPackets.SPlayerData, "index": index, "sprite": 0,
                        "name": "", "access": 0, "map": 0, "x": 0, "y": 0, "direction": 0}])
    g.conn.sendDataToAllBut(index, packet)


def sendBlock():
    packet = json.dumps([{"packet": ServerPackets.SBeginBlock}])
    g.conn.sendDataToAll(packet)
    for b in g.game.space.bodies:

        # log('ID :' + str(b._id_counter))
        # log('Position :' + str(b._get_position()))
        # log('Rot Vect :' + str(b._get_rotation_vector()))
        # log('BodyType :' + str(b._get_type()))
        packet = json.dumps([{"packet": ServerPackets.SSendBlock, "ID": b._id_counter,
                             "positionX": b._get_position().x, "positionY": b._get_position().y, "rotationX": b._get_rotation_vector().x, "rotationY": b._get_rotation_vector().y}])
        g.conn.sendDataToAll(packet)
    packet = json.dumps([{"packet": ServerPackets.SEndBlock}])
    g.conn.sendDataToAll(packet)
