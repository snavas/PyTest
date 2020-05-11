# import required libraries
from vidgear.gears import VideoGear
from vidgear.gears import NetGear
from classes.realsense import RealSense
import numpy as np
import cv2

# open any valid video stream(for e.g `test.mp4` file)
#stream = VideoGear(source='test.mp4').start()
device = RealSense("752112070399")

# activate bidirectional mode
options = {'bidirectional_mode': True}

# Define Netgear Server with defined parameters
server = NetGear(pattern=1, logging=True, **options)

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

        # check data just received from Client is of numpy datatype
        if not (recv_data is None) and isinstance(recv_data, np.ndarray):
            # {do something with received numpy array here}

            # Let's show it on output window
            cv2.imshow("Output Frame", recv_data)
            key = cv2.waitKey(1) & 0xFF

    except KeyboardInterrupt:
        break

# safely close video stream
device.stop()

# safely close server
server.close()