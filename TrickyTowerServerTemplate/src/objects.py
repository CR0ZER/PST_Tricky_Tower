from typing_extensions import Self
from constants import *
import global_vars as g
import pymunk


class Player():
    def __init__(self):
        self.move = 0
        self.state = 0
        self.dropSpeed = 10


class Game():
    def __init__(self):
        self.nbplayer = 0
        self.players = [Player() for i in range(MAX_PLAYERS)]
        self.space = pymunk.Space()
        self.space.gravity = 0, -98
        self.body = None       # Create a Body
        self.poly = None

    def lauch(self):
        self.body = pymunk.Body()
        self.body.position = 500, 100      # Set the position of the body

        # Create a box shape and attach to body
        self.poly = pymunk.Poly.create_box(self.body)
        self.poly.mass = 10              # Set the mass on the shape
        # Set the mass on the shape
        self.space.add(self.body, self.poly)


# class Board():
#    def __init__(self):
#        self.playerPosition = 0
#
#    def createBox(self):
#        body = pymunk.Body()        # Create a Body
#        body.position = 500, 500      # Set the position of the body
#
#        # Create a box shape and attach to body
#        poly = pymunk.Poly.create_box(body)
#        poly.mass = 10              # Set the mass on the shape
        # space.add(body, poly)            # Set the mass on the shape


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
