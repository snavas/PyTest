#!/usr/bin/python
import socket, videosocket
from io import StringIO ## for Python 3
from videofeed import VideoFeed

class Client:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(("localhost", 6000))
        self.vsock = videosocket.videosocket (self.client_socket)
        self.videofeed = VideoFeed(1,"client",1)
        self.data = StringIO()

    def connect(self):
        while True:
            frame=self.videofeed.get_frame()
            self.vsock.vsend(frame)
            frame = self.vsock.vreceive()
            self.videofeed.set_frame(frame)
                
if __name__ == "__main__":
    client = Client()
    client.connect()
