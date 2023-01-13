
class ClientPackets:
    CLogin, CQuit, CLaunch, CArrowKey, CNewPlayer = range(5)


class ServerPackets:
    SLoginOK, SSendBlock, SBeginBlock, SEndBlock, SPlayerCount, SGameStart, SWinner = range(
        7)
