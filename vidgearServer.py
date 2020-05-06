# import libraries
from classes.vidserver import VidServer
from classes.realsense import RealSense
import libs.hand as hand
import libs.draw as draw
import cv2

device = RealSense("821212062065")
server = VidServer()

# infinite loop until [Ctrl+C] is pressed
while True:
    try:
        # read frames
        colorframe = device.getcolorstream()
        depthframe = device.getdepthstream()
        # check if frame is None
        if colorframe is None:
            #if True break the infinite loop
            break
        # do something with frame here
        result, hands, points = hand.getHand(colorframe, depthframe, device.getdepthscale())
        if hands:
            cv2.drawContours(result, hands, -1, (0, 255, 0), 2)
            for p in points:
                cv2.circle(result, tuple(p), 2, (0, 0, 255))
        drawings = draw.getDraw(colorframe)
        # send frame to server
        #server.send(result)
        server.send(cv2.bitwise_or(result, drawings))
    except KeyboardInterrupt:
        #break the infinite loop
        break

# safely close video stream
device.stop()
# safely close serverWWW
server.close()