from twisted.internet import reactor, protocol

HOST = 'localhost'
PORT = 8000

class MyClient(protocol.Protocol):



    def connectionMade(self):
        # Placeholder testing sending data to the server
        command = b'0:on'
        self.transport.write(command)
    
    
    
    def dataReceived(self, data):
        #As soon as any data is received, write it back.
        print("Server said:", data)

    
    
    def connectionLost(self, reason):
        print("connection lost")



    def ClientDisconnect(self):
        self.transport.loseConnection()



class MyClientFactory(protocol.ClientFactory):
    protocol = MyClient

factory = MyClientFactory()
reactor.connectTCP(HOST, PORT, factory)

reactor.run()


