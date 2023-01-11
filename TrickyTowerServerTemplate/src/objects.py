from typing_extensions import Self
from constants import *
import global_vars as g
import pymunk
import random


class Player():
    def __init__(self):
        self.move = 0
        self.state = 0
        self.dropSpeed = 10


class Block():
    def __init__(self):
        self.body = None
        self.shape1 = None
        self.shape2 = None
        self.type = None


class Game():
    def __init__(self):
        self.nbplayer = 0
        self.players = [Player() for i in range(MAX_PLAYERS)]
        self.space = pymunk.Space()
        self.space.gravity = 0, 200
        self.static_Blocks = []  # Create a Body
        self.blocks = []

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

    def createRamdomBlock(self, player):
        self.blocks.append(Block())
        self.blocks[-1].body = pymunk.Body()
        self.blocks[-1].body.position = 105+player*250, 500

        r = random.randint(1, 7)
        self.blocks[-1].type = r

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
                    box2 = [(10, 0), (20, 0), (20, 10), (10, 10)]
                elif r == 6:
                    box = [(10, 0), (20, 0), (20, 30), (10, 30)]
                    box2 = [(0, 0), (10, 0), (10, 10), (0, 10)]
                else:
                    box = [(0, 10), (30, 10), (30, 20), (0, 20)]
                    box2 = [(10, 0), (20, 0), (20, 10), (10, 10)]
                self.blocks[-1].shape1 = pymunk.Poly(self.blocks[-1].body, box)
                self.blocks[-1].shape1.mass = 3 * MASS_MULTIPLIER
                self.blocks[-1].shape1.friction = BLOCK_FRICTION
                self.blocks[-1].shape2 = pymunk.Poly(
                    self.blocks[-1].body, box2)
                self.blocks[-1].shape2.mass = 1 * MASS_MULTIPLIER
                self.blocks[-1].shape2.friction = BLOCK_FRICTION

                self.space.add(
                    self.blocks[-1].body, self.blocks[-1].shape1, self.blocks[-1].shape2)
                return
            self.blocks[-1].shape1 = pymunk.Poly(self.blocks[-1].body, box)
            self.blocks[-1].shape1.mass = 2 * MASS_MULTIPLIER
            self.blocks[-1].shape1.friction = BLOCK_FRICTION
            self.blocks[-1].shape2 = pymunk.Poly(self.blocks[-1].body, box2)
            self.blocks[-1].shape2.mass = 2 * MASS_MULTIPLIER
            self.blocks[-1].shape2.friction = BLOCK_FRICTION

            self.space.add(
                self.blocks[-1].body, self.blocks[-1].shape1, self.blocks[-1].shape2)
            return

        self.blocks[-1].body.position = 105+player*250, 500
        self.blocks[-1].shape1 = pymunk.Poly(
            self.blocks[-1].body, box)
        self.blocks[-1].shape1.mass = 4 * MASS_MULTIPLIER
        self.blocks[-1].shape1.friction = BLOCK_FRICTION
        self.space.add(self.blocks[-1].body, self.blocks[-1].shape1)


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
