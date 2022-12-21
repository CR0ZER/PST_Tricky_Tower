# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

 
from genericpath import getmtime
from secrets import token_bytes
from xml.etree.ElementTree import tostring
from twisted.internet import protocol, reactor


class Echo(protocol.Protocol):
    """This is just about the simplest possible protocol"""
    Echo_a = 1
    
    def dataReceived(self, data):
        "As soon as any data is received, write it back."
        if self.Echo_a >= 4:
            self.Echo_a = self.Echo_a - 2
        else:
            self.Echo_a += 1
        self.transport.write(self.Echo_a.to_bytes())


def main():
    """This runs the protocol on port 8000"""
    factory = protocol.ServerFactory()
    factory.protocol = Echo
    reactor.listenTCP(8000, factory)
    reactor.run()


# this only runs if the module was *not* imported
if __name__ == "__main__":
    main()
