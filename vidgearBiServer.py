# import required libraries
#from vidgear.gears import VideoGear
from vidgear.gears import NetGear
from classes.realsense import RealSense
import libs.hand as hand
import libs.draw as draw
import numpy as np
import cv2, asyncio, base64

import base64
import skimage.io

def decode(base64_string):
    if isinstance(base64_string, bytes):
        base64_string = base64_string.decode("utf-8")

    imgdata = base64.b64decode(base64_string)
    img = skimage.io.imread(imgdata, plugin='imageio')
    return img

# open any valid video stream(for e.g `test.mp4` file)
#stream = VideoGear(source='C:\saest.mp4').start()
device = RealSense("752112070399")

# activate bidirectional mode
options = {'bidirectional_mode': True}

# Define Netgear Server with defined parameters
# server = NetGear(pattern=1, logging=True, **options) # LOCAL
server = NetGear(address = '0.tcp.eu.ngrok.io', port = '12920', protocol = 'tcp',  pattern = 1, logging = True, **options)

# loop over until KeyBoard Interrupted
while True:

    try:

        # read frames from stream
        frame = device.getcolorstream()

        # check for frame if Nonetype
        if frame is None:
            break

        # {do something with the frame here}

        # prepare data to be sent(a simple text in our case)
        target_data = 'Hello, I am a Server.'

        # send frame & data and also receive data from Client
        recv_data = server.send(frame, message=target_data)

        # print data just received from Client
        if not (recv_data is None):
            #print(recv_data)
            result = decode(recv_data)
            cv2.imshow("Output Frame", result)

        # check for 'q' key if pressed
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

    except KeyboardInterrupt:
        break

# safely close video stream
device.stop()

#
cv2.destroyAllWindows()

# safely close server
server.close()