from constants import *


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
