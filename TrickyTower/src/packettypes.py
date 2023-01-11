class ClientPackets:
    CLogin, CQuit, CLaunch = range(3)


class ServerPackets:
    SLoginOK, SSendBlock, SBeginBlock, SEndBlock, SPlayerCount = range(5)
