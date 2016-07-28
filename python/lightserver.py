from twisted.internet import reactor, protocol
import serial

PORT = 8000

class MyServer(protocol.Protocol):
    print ('Starting server...')
    
    
    def connectionMade(self):
        self.curClient = self
        
        # Add to the active clients list
        self.factory.clients.append(self)
        # Print all currently connected clients
        print (self.factory.clients)
    
    
    # This keeps our active client list from becoming saturated with carcases
    def connectionLost(self, reason):
        print ('Client ' + str(self.curClient) + ' has quit')
        
        # Remove from active clients list
        self.factory.clients.remove(self.curClient)
    
    
    def dataReceived(self, data):
        try:
            self.parseClientData(data)
        except:
            print ('Something went wrong...')
        
        ### THIS IS TEMPORARY!!! ###
        # Send a message back to the client that we got the data!
        self.broadcastData('We got your message! ')
    
    
    # Send data to all active clients
    def broadcastData(self, data):
        broadcastMSG = str.encode(data)
        for client in self.factory.clients:    
            client.transport.write(broadcastMSG) 
    
    
    # Send data to only the current client
    def sendData(self, data):
        MSG = str.encode(data)
        self.transport.write(MSG)
    
    
    def parseClientData(self, data):
        container = bytes.decode(data)
        
        # Lamp ID first, power state last
        
        # Multiple commands (Check if we have proper container,
        # cmd and arg delimiters)
        if '|' in container and ':' in container:
            print ('Multiple commands')
            container = container.split("|")
            self.splitContainers(container)
            
        # Single command
        else:
            print ('Single command')
            self.splitCmdArgs(container)
            
            
    # Splits up containers (Used when we have multiple
    # commands sent at once)
    def splitContainers(self, container):
        for containers in container:
            self.splitCmdArgs(containers)
    
    
    # Splits command and argument(s) appropriately
    def splitCmdArgs(self, args):
        if ':' in args:
            
            count = 0
            command = ''
            argument = ''
            
            args = args.split(':')
            for value in args:
                print (count)
    
                if count == 0:
                    command = value
                elif count == 1:
                    argument = value
    
                count =+ 1
                #print (command)
                #print (argument)

                self.interpretCmd(command, argument)
    
    
    # Actually do something with the arguments...
    def interpretCmd(self, cmd, arg):
        print ('LampID: ' + str(cmd))
        print ('State: ' + str(arg))
    
    
class MyServerFactory(protocol.Factory):
    protocol = MyServer
    clients = []
    
    ### Add more lamp IDs between here! ###
    
    lampID0 = 0
    lampID1 = 1
    lampID2 = 2
    
    ### Add more lamp IDs between here! ###
    
    # Lamp state (Obviously...)
    ON = 0
    OFF =1
    
factory = MyServerFactory()
reactor.listenTCP(PORT, factory)
reactor.run()

