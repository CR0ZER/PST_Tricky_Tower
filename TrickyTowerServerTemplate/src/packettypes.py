
class ClientPackets:
    CLogin, CQuit, CLaunch, CArrowKey, CNewPlayer = range(5)


class ServerPackets:
    SLoginOK, SSendBlock, SBeginBlock, SEndBlock, SPlayerCount = range(5)
