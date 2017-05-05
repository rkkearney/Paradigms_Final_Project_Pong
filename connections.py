from twisted.internet.protocol import Factory
from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
from twisted.internet.defer import DeferredQueue
from twisted.internet.task import LoopingCall
from twisted.internet import reactor

# for listener
class HostConnFactory(Factory):
    def __init__(self, gamespace):
        self.gamespace = gamespace

    def buildProtocol(self, addr):
        self.addr = addr
        self.conn = HostConnection(addr, self.gamespace)
        return self.conn

class HostConnection(Protocol):
    def __init__(self, addr, gamespace):
        self.addr = addr
        self.gamespace = gamespace

    def connectionMade(self):
        print "connection made"
        # run the game til events end it
        self.gamespace.main()
        looping = LoopingCall(self.gamespace.tick()) #makes all the ticks?
        looping.start(1/60)

    def dataReceived(self, data):
        #add data to some function in gamspace
        #send it to the addingData function to integrate to board
        pass

    def sendData(self, data):
        self.transport.write(data)

    def connectionLost(self):
        print "connection lost"

# other side (Client?)
class ClientConnFactory(ClientFactory):
    def __init__(self, gamespace):
        self.gamespace = gamespace
    
    def buildProtocol(self, addr):
        self.addr = addr
        self.conn = ClientConnection(addr, self.gamespace)
        return self.conn

class ClientConnection(Protocol):
    def __init__(self, addr, gamespace):
        self.addr = addr
        self.gamespace = gamespace

    def connectionMade(self):
        print "connection 2 made"
        # run the game til events end it
        self.gamespace.main()
        looping = LoopingCall(self.gamespace.tick()) #makes all the ticks?
        looping.start(1/60)

    def dataReceived(self, data):
        #add data to some function in gamspace
        #function called addingData
        pass

    def sendData(self, data):
        self.transport.write(data)

    def connectionLost(self):
        print "connection 2 lost"


