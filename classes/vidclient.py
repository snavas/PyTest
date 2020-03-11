from classes.network import Network
from vidgear.gears import NetGear

class VidClient(Network):

    # overriding abstract method
    def __init__(self):
        self.client = NetGear(receive_mode=True)

    # overriding abstract method
    def recieve(self):
        return self.client.recv()

    # overriding abstract method
    def stop(self):
        self.client.stop()
