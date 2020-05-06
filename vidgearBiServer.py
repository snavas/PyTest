# import required libraries
from classes.realsense import RealSense
from vidgear.gears import NetGear
import libs.hand as hand
import libs.draw as draw
import cv2

# open any valid video stream(for e.g `test.mp4` file)
device = RealSense("821212062065")

# activate bidirectional mode
options = {'bidirectional_mode': True}

# Define Netgear Server with defined parameters
server = NetGear(pattern=1, logging=True, **options)

# loop over until KeyBoard Interrupted
while True:

    try:
        # read frames
        colorframe = device.getcolorstream()
        depthframe = device.getdepthstream()

        # check for frame if Nonetype
        if colorframe is None:
            break

        # do something with frame here
        result, hands, points = hand.getHand(colorframe, depthframe, device.getdepthscale())
        if hands:
            cv2.drawContours(result, hands, -1, (0, 255, 0), 2)
            for p in points:
                cv2.circle(result, tuple(p), 2, (0, 0, 255))
        drawings = draw.getDraw(colorframe)

        # prepare data to be sent(a simple text in our case)
        #target_data = 'Hello, I am a Server.'

        # send frame & data and also receive data from Client
        #recv_data = server.send(frame, message=target_data)
        recv_data = server.send(cv2.bitwise_or(result, drawings))

        # print data just received from Client
        if not (recv_data is None):
            cv2.imshow("Output Frame", recv_data)

    except KeyboardInterrupt:
        break

# safely close video stream
device.stop()

# close output window
cv2.destroyAllWindows()

# safely close server
server.close()