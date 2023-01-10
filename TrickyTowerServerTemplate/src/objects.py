from constants import *
import pymunk

space = pymunk.Space()
space.gravity = 0, 98


class Board():
    def __init__(self):
        self.playerPosition = 0
        self.dropSpeed = 10

    def createBox(self):
        body = pymunk.Body()        # Create a Body
        body.position = 500, 500      # Set the position of the body

        # Create a box shape and attach to body
        poly = pymunk.Poly.create_box(body)
        poly.mass = 10              # Set the mass on the shape
        space.add(body, poly)            # Set the mass on the shape


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


Player = [AccountClass() for i in range(MAX_PLAYERS)]
TempPlayer = [TempPlayerClass() for i in range(MAX_PLAYERS)]
