from classes.network import Network
from vidgear.gears import NetGear

class VidServer(Network):

    # overriding abstract method
    def __init__(self):
        self.server = NetGear(receive_mode=False)

    # overriding abstract method
    def send(self, data):
        self.server.send(data)

    # overriding abstract method
    def stop(self):
        self.server.stop()
