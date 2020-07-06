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
import numpy as np
import zmq
import socket
import asyncio
import sys
import argparse
import base64
from classes.peer import Peer

MSGLEN = 1221248

def send(s, msg):
    totalsent = 0
    while totalsent < MSGLEN:
        sent = s.send(msg[totalsent:])
        if sent == 0:
            raise RuntimeError("socket connection broken")
        totalsent = totalsent + sent

@asyncio.coroutine
async def recieve_frame(s):
    s.listen(1)  # Now wait for client connection.
    while True:
        c, addr = s.accept()  # Establish connection with client.
        chunks = []
        bytes_recd = 0
        while bytes_recd < MSGLEN:
            chunk = s.recv(min(MSGLEN - bytes_recd, 2048))
            if chunk == b'':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
        frame = b''.join(chunks)
        c.close()
        cv2.namedWindow('RealSense', cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("RealSense", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.imshow('RealSense', frame)
        cv2.waitKey(1)

def main():
    device = RealSense("752112070204")
    listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_sock.bind(('localhost', 5551))
    writing_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    writing_sock.bind(('localhost', 5552))
    loop = asyncio.get_event_loop()
    print("Color intrinsics: ", device.getcolorintrinsics())
    print("Depth intrinsics: ", device.getdepthintrinsics())
    try:
        loop.run_until_complete(recieve_frame(listen_sock))
        loop.run_forever()
        while True:
            writing_sock.connect(('localhost', 5555))
            colorframe = device.getcolorstream()
            depthframe = device.getdepthstream()
            result, hands, points = hand.getHand(colorframe, depthframe, device.getdepthscale())
            if hands:
                cv2.drawContours(result, hands, -1, (0,255,0), 2)
                for p in points:
                    cv2.circle(result, tuple(p), 2, (0, 0, 255))
            send(writing_sock, result)
    except KeyboardInterrupt:
        pass
    finally:
        # Stop streaming
        device.stop()
        loop.close()

if __name__ == '__main__':
    main()