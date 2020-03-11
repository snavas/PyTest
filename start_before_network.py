## License: Apache 2.0. See LICENSE file in root directory.
## Copyright(c) 2015-2017 Intel Corporation. All Rights Reserved.

# useufl: https://dev.to/amarlearning/finger-detection-and-tracking-using-opencv-and-python-586m
# https://www.amazon.de/dp/B07L2XZSWD
# https://www.amazon.de/dp/B01HAXUHQ6/

#import pyrealsense2 as rs
#import numpy as np
import cv2
from classes.realsense import RealSense
import libs.hand as hand
from classes.peer import Peer


#import screeninfo

def main():
    device = RealSense()
    #connection = Peer()
    #connection.makeserversocket(5050)
    print("Color intrinsics: ", device.getcolorintrinsics())
    print("Depth intrinsics: ", device.getdepthintrinsics())
    try:
        while True:
            # clientsock, clientaddr = connection.accept()
            colorframe = device.getcolorstream()
            depthframe = device.getdepthstream()

            result, hands, points = hand.getHand(colorframe, depthframe, device.getdepthscale())

            cv2.namedWindow('RealSense', cv2.WND_PROP_FULLSCREEN)
            cv2.setWindowProperty("RealSense", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            if hands:
                cv2.drawContours(result, hands, -1, (0,255,0), 2)
                for p in points:
                    cv2.circle(result, tuple(p), 2, (0, 0, 255))
            cv2.imshow('RealSense', result)
            cv2.waitKey(1)

    finally:
        # Stop streaming
        device.stop()

if __name__ == '__main__':
    main()