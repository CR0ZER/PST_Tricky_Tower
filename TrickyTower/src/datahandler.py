import global_vars as g
from constants import *
from packettypes import *



class DataHandler():
    ''' class for handling data sent from the server '''

    def __init__(self, protocol=2):
        self.protocol = protocol

    def handleData(self, data):
        jsonData = decodeJSON(data)
        packetType = jsonData[0]["packet"]

        if packetType == ServerPackets.SLoginOK:
            self.handleSLoginOK(jsonData)

        elif packetType == ServerPackets.SLoginOK:
            self.handleSLoginOK(jsonData)

        else:
            # Packet is unknown - hacking attempt
            print "hacking attempt"

    def handleAlertMsg(self, jsonData):
        msg = jsonData[0]['msg']

        print msg
