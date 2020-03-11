# https://stackoverflow.com/questions/24718111/webrtc-with-python
# https://github.com/aiortc/aiortc
# http://cs.berry.edu/~nhamid/p2p/framework-python.html

import socket

class Peer:
    def __init__(self, maxpeers, serverport, myid=None, serverhost = None ):
        self.debug = 0
        self.maxpeers = int(maxpeers)
        self.serverport = int(serverport)
        # If not supplied, the host name/IP address will be determined
        # by attempting to connect to an Internet host like Google.
        if serverhost: self.serverport = serverhost
        else: self.__initserverhost()
        # If not supplied, the peer id will be composed of the host address
        # and port number
        if myid: self.myid = myid
        else: self.myid = '%s:%d' % (self.serverhost, self.serverport)
        # list (dictionary/hash table) of known peers
        self.peers = {}
        # used to stop the main loop
        self.shutdown = False
        self.handlers = {}
        self.router = None
        # end constructor

    def __initserverhost(self):
        # Attempt to connect to an Internet host in order to determine the local machine's IP address.
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("www.google.com", 80))
        self.serverhost = s.getsockname()[0]
        s.close()

    def makeserversocket( self, port, backlog=5 ):
        s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        s.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
        s.bind( ( '', port ) )
        s.listen( backlog )
        return s
