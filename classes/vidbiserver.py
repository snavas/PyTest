from classes.network import Network
from vidgear.gears import NetGear

class VidServer(Network):

    # overriding abstract method
    def __init__(self):
        options = {'bidirectional_mode': True}
        self.server = NetGear(pattern = 1, logging = True, **options)

    # overriding abstract method
    def send(self, data):
        return self.server.send(data)

    # overriding abstract method
    def stop(self):
        self.server.stop()
