## License: Apache 2.0. See LICENSE file in root directory.
## Copyright(c) 2015-2017 Intel Corporation. All Rights Reserved.

#import pyrealsense2 as rs
#import numpy as np
import cv2
from classes.realsense import RealSense
from classes.objloader import *
import copy
import numpy as np
#import screeninfo

def main():
    MIN_MATCHES = 15
    device = RealSense()
    model = cv2.imread('models/rolex.jpg', 0)
    #print("Color intrinsics: ", device.getcolorintrinsics())
    #print("Depth intrinsics: ", device.getdepthintrinsics())
    # Initiate ORB detector
    orb = cv2.ORB_create()
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    kp_model, des_model = orb.detectAndCompute(model, None)

    try:
        while True:
            image = device.getcolorstream()

            # Feature Extraction
            #kp = orb.detect(image, None) # find the keypoints with ORB
            #kp, des = orb.compute(image, kp) # compute the descriptors with ORB
            #image2 = cv2.drawKeypoints(image, kp, image, color=(0, 255, 0), flags=0) # draw only keypoints location,not size and orientation
            kp_frame, des_frame = orb.detectAndCompute(image, None)
            matches = bf.match(des_model, des_frame)
            matches = sorted(matches, key=lambda x: x.distance)
            # compute Homography if enough matches are found
            if len(matches) > MIN_MATCHES:
                src_pts = np.float32([kp_model[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
                dst_pts = np.float32([kp_frame[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)
                M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
                h, w = model.shape
                pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
                dst = cv2.perspectiveTransform(pts, M)

                #image2 = cv2.polylines(image, [np.int32(dst)], True, 255, 3, cv2.LINE_AA)
                image2 = cv2.drawMatches(model, kp_model, image, kp_frame, matches[:MIN_MATCHES], 0, flags=2)
                # Show images
                cv2.namedWindow('RealSense', cv2.WND_PROP_FULLSCREEN)
                cv2.setWindowProperty("RealSense", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                cv2.imshow('RealSense', image2)
                cv2.waitKey(1)
            else:
                print("Not enough matches found - %d/%d" % (len(matches), MIN_MATCHES))

    finally:
        # Stop streaming
        device.stop()

if __name__ == '__main__':
    main()