
class ClientPackets:
    CLogin, CQuit, CLaunch, CArrowKey = range(4)


class ServerPackets:
    SLoginOK, SSendBlock, SBeginBlock, SEndBlock, SPlayerCount = range(5)
