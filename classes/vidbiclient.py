from classes.network import Network
from vidgear.gears import NetGear

class VidClient(Network):

    # overriding abstract method
    def __init__(self):
        options = {'bidirectional_mode': True}
        self.client = NetGear(receive_mode = True, pattern = 1, logging = True, **options)

    # overriding abstract method
    def recieve(self, data):
        return self.client.recv()

    # overriding abstract method
    def stop(self):
        self.client.stop()
