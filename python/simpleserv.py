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

        #try:
        self.parseClientData(data)
        #except:
        #    print ('Something went wrong...')

    
        ### THIS IS TEMPORARY!!! ###
        # Send a message back to the client that we got the data!
        self.broadcastData('We got your message! ')
        
    

    # Send data to all currently connected clients
    def broadcastData(self, data):
        broadcastMSG = str.encode(data)
        for client in self.factory.clients:    
            client.transport.write(broadcastMSG) 



    # Send data to only the current client
    def sendData(self, data):
        MSG = str.encode(data)
        self.transport.write(MSG)



    def parseClientData(self, data):
        cmds = bytes.decode(data)
        
        # The lamp ID comes first than the power state
        
        # Multiple commands
        if '|' in cmds:
            print ('Multiple strings')
            cmds = cmds.split("|")
            print (cmds)
            #self.splitCmds(cmds)
            
        # Single command
        else:
            print ('Single string')
            #self.splitCmds(cmds)
            print (cmds)
             
             
             
    # Split up individual commands with args
    def splitCmds(self, cmds):
        for x in cmds:
            cmds = x.split(":")
            print (x)


    # Actually do something with the arguments
    def interpretCmd(self, lampID, state):
        print ('Do nothing...')



class MyServerFactory(protocol.Factory):
    protocol = MyServer
    clients = []

    lampID0 = 0
    lampID1 = 1
    lampID2 = 2



factory = MyServerFactory()
reactor.listenTCP(PORT, factory)
reactor.run()


