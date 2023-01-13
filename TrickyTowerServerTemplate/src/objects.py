from typing_extensions import Self
from constants import *
import global_vars as g
import pymunk

import random
from utils import *

from pymunk.vec2d import *


class Player():
    def __init__(self):
        self.key = []
        self.state = 0
        self.dropSpeed = 10
        self.block = None
        self.BeginWinTime = None
        self.clockMovementLeft = None
        self.clockMovementRight = None
        for i in range(5):
            self.key.append(False)


class Block():
    def __init__(self):
        self.body = None
        self.shape1 = None
        self.shape2 = None
        self.type = None


def doCollide(shape1, shape2):
    if shape1 == None or shape2 == None:
        return False
    col = shape1.shapes_collide(shape2)
    if (len(col.points) >= 1):
        # Ultra weird shit happen when tetris piece 5 or 6 are summoned so if !=0 is IMPORTANT
        if col.points[0].distance != 0.0:
            return True
    return False


class Game():
    def __init__(self):
        self.nbplayer = 0
        self.players = [Player() for i in range(MAX_PLAYERS)]
        self.space = pymunk.Space()
        self.space.gravity = 0, 200
        self.space.sleep_time_threshold = 30
        self.static_Blocks = []  # Create a Body
        self.blocks = []

    def areYaWinningSon(self, index):
        s = self.space.segment_query_first(
            (index*250, WIN_HEIGHT), ((index + 1)*250, WIN_HEIGHT), 0.0, pymunk.ShapeFilter(categories=0x1))
        if s:
            if self.players[index].BeginWinTime == None:
                self.players[index].BeginWinTime = g.clockTime
            elif self.players[index].BeginWinTime + 3 < g.clockTime:
                log("player " + str(index) + " WIN !")
                return False
        else:
            self.players[index].BeginWinTime = None
        return True

    def playerMove(self, index):
        p = self.players[index]
        p.block.body.position += Vec2d(0, p.dropSpeed)
        p.dropSpeed = DROP_SPEED

    def playerInput(self, index):
        p = self.players[index]

        if p.key[DIR_UP] == True:  # rotate
            p.block.body.angle += 1.57079632679  # Pi/2
            p.key[DIR_UP] = False

        if p.key[DIR_LEFT] == True:  # move left
            if p.clockMovementLeft == None:
                p.clockMovementLeft = g.clockTime
                p.block.body.position -= Vec2d(5, 0)
            elif p.clockMovementLeft + HORIZONTAL_TICK_MOV < g.clockTime:
                p.clockMovementLeft = None
        if p.key[DIR_LEFT] == False:
            p.clockMovementLeft = None

        if p.key[DIR_DOWN] == True:  # speed up descent
            p.dropSpeed = BOOST_DROP_SPEED

        if p.key[DIR_RIGHT] == True:  # move right
            if p.clockMovementRight == None:
                p.clockMovementRight = g.clockTime
                p.block.body.position += Vec2d(5, 0)
            elif p.clockMovementRight + HORIZONTAL_TICK_MOV < g.clockTime:
                p.clockMovementRight = None
        if p.key[DIR_RIGHT] == False:
            p.clockMovementRight = None

    def checkPlayerCollide(self, index):
        p = self.players[index]
        if doCollide(p.block.shape1, self.static_Blocks[index].shape1) or doCollide(p.block.shape2, self.static_Blocks[index].shape1):
            p.block.body.activate()
            self.blocks.append(p.block)
            p.block = None
            self.createRamdomBlock(index)
            return

        for b in self.blocks:
            if doCollide(p.block.shape1, b.shape1) or doCollide(p.block.shape1, b.shape2) or doCollide(p.block.shape2, b.shape1) or doCollide(p.block.shape2, b.shape2):
                p.block.body.activate()
                self.blocks.append(p.block)
                p.block = None
                self.createRamdomBlock(index)
                return
        if (p.block.body.is_sleeping == False):
            p.block.body.sleep()

    def launch(self):
        for i in range(4):
            self.static_Blocks.append(Block())
            self.static_Blocks[i].type = 0
            self.static_Blocks[i].body = pymunk.Body(
                body_type=pymunk.Body.STATIC)
            box = [(0, 0), (70, 0), (70, 10), (0, 10)]
            self.static_Blocks[i].shape1 = pymunk.Poly(
                self.static_Blocks[i].body, box)
            self.static_Blocks[i].shape1.friction = PLATE_FRICTION
            self.static_Blocks[i].body.position = 70+i*250, 700
            self.space.add(
                self.static_Blocks[i].body, self.static_Blocks[i].shape1)
            self.createRamdomBlock(i)

    def removeFalledBlocks(self):
        for b in self.blocks:
            if b.body.position.y > 750:
                if b.type >= 3:
                    self.space.remove(b.body, b.shape1, b.shape2)
                else:
                    self.space.remove(b.body, b.shape1)
                self.blocks.remove(b)
        for i in range(MAX_PLAYERS):
            if self.players[i].block.body.position.y > 730:
                if self.players[i].block.type >= 3:
                    self.space.remove(
                        self.players[i].block.body, self.players[i].block.shape1, self.players[i].block.shape2)
                else:
                    self.space.remove(
                        self.players[i].block.body, self.players[i].block.shape1)
                self.createRamdomBlock(i)

    def createRamdomBlock(self, index):
        self.players[index].block = Block()
        self.players[index].block.body = pymunk.Body()
        self.players[index].block.body.position = 105+index*250, 300

        r = random.randint(1, 7)
        self.players[index].block.type = r

        if r == 1:
            box = [(0, 0), (0, 40), (10, 40), (10, 0)]

        elif r == 2:
            box = [(0, 0), (0, 20), (20, 20), (20, 0)]

        else:
            if r == 3:
                box = [(0, 0), (20, 0), (20, 10), (0, 10)]
                box2 = [(10, 10), (30, 10), (30, 20), (10, 20)]
            elif r == 4:
                box = [(10, 0), (30, 0), (30, 10), (10, 10)]
                box2 = [(0, 10), (20, 10), (20, 20), (0, 20)]
            else:
                if r == 5:
                    box = [(0, 0), (10, 0), (10, 30), (0, 30)]
                    box2 = [(20, 0), (20, 10), (10, 10), (10, 0)]
                elif r == 6:
                    box = [(10, 0), (20, 0), (20, 30), (10, 30)]
                    box2 = [(0, 0), (10, 0), (10, 10), (0, 10)]
                else:
                    box = [(0, 10), (30, 10), (30, 20), (0, 20)]
                    box2 = [(10, 0), (20, 0), (20, 10), (10, 10)]
                self.players[index].block.shape1 = pymunk.Poly(
                    self.players[index].block.body, box)
                self.players[index].block.shape1.mass = 3 * MASS_MULTIPLIER
                self.players[index].block.friction = BLOCK_FRICTION
                self.players[index].block.shape2 = pymunk.Poly(
                    self.players[index].block.body, box2)
                self.players[index].block.shape2.mass = 1 * MASS_MULTIPLIER
                self.players[index].block.shape2.friction = BLOCK_FRICTION

                self.space.add(
                    self.players[index].block.body, self.players[index].block.shape1, self.players[index].block.shape2)
                self.players[index].block.body.sleep()
                return
            self.players[index].block.shape1 = pymunk.Poly(
                self.players[index].block.body, box)
            self.players[index].block.shape1.mass = 2 * MASS_MULTIPLIER
            self.players[index].block.shape1.friction = BLOCK_FRICTION
            self.players[index].block.shape2 = pymunk.Poly(
                self.players[index].block.body, box2)
            self.players[index].block.shape2.mass = 2 * MASS_MULTIPLIER
            self.players[index].block.shape2.friction = BLOCK_FRICTION

            self.space.add(
                self.players[index].block.body, self.players[index].block.shape1, self.players[index].block.shape2)
            self.players[index].block.body.sleep()
            return

        self.players[index].block.shape1 = pymunk.Poly(
            self.players[index].block.body, box)
        self.players[index].block.shape1.mass = 4 * MASS_MULTIPLIER
        self.players[index].block.shape1.friction = BLOCK_FRICTION

        self.space.add(self.players[index].block.body,
                       self.players[index].block.shape1)
        self.players[index].block.body.sleep()


class AccountClass():
    def __init__(self):
        # Account
        self.Login = ""
        self.Password = None


class TempPlayerClass():
    def __init__(self):
        # Non saved, local variables
        self.Buffer = None
        self.charNum = 0
        self.inGame = False

        self.partyPlayer = None
        self.inParty = False

        self.dataTimer = None
        self.dataBytes = None
        self.dataPackets = None
