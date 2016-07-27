from twisted.internet import reactor, protocol

PORT = 8000

class MyServer(protocol.Protocol):
    print ('Starting server...')



    def connectionMade(self):
        self.curClient = self

        # Add to the active clients list
        self.factory.clients.append(self)
        # Print all currently connected clients
        print (self.factory.clients)



    def connectionLost(self, reason):
        print ('Client ' + str(self.curClient) + ' has quit')
        
        # Remove from active clients list
        self.factory.clients.remove(self.curClient)



    def dataReceived(self, data):
        try:
            self.parseClientData(data)
        except:
            pass
    
        ### THIS IS TEMPORARY!!! ###
        bits = str.encode('We got your message! ')
        "Send a message back to the client that we got the data!"
        self.broadcastData(bits)
        
    

    # Send data to all currently connected clients
    def broadcastData(self, data):
        for client in self.factory.clients:    
            broadcastMSG = str.encode('Hello clients!')
            client.transport.write(broadcastMSG) 



    # Send data to only the current client
    def sendData(self, data):
        self.transport.write(data)



    def parseClientData(self, data):
        data = bytes.decode(data)
        
        # The lamp ID comes first than the power state
        
        
        if ':' in data:
            # Light args
            args = data.split(":", 1)

            # Lamp ID
            print (args[0])
            
            # Power state
            print (args[1])



class MyServerFactory(protocol.Factory):
    protocol = MyServer
    clients = []

    lampID0 = 0
    lampID1 = 0
    lampID2 = 0



factory = MyServerFactory()
reactor.listenTCP(PORT, factory)
reactor.run()


