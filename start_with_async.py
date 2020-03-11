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

recievedframe = []
device = []

def getOptions(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description="Parses command.")
    parser.add_argument("-c", "--create", help="Create session (Default)")
    parser.add_argument("-j", "--join", type=str, help="Join session XXX.XXX.XXX.XXX")
    options = parser.parse_args(args)
    return options

options = getOptions(sys.argv[1:])
if options.join: ip = options.join
else: ip = "localhost"

async def sendFrame(message, writer):
    #print(f'Send: {message!r}')
    writer.write(message.encode())
    await writer.drain()

async def recieveFrame(reader):
    data = await reader.read(100)
    print(f'Received: {data.decode()!r}')
    recievedframe = data.decode()

async def handle_client(reader, writer):
    #data = await reader.read(-1)
    #recievedframe = data.decode()
    colorframe = device.getcolorstream()
    depthframe = device.getdepthstream()
    result, hands, points = hand.getHand(colorframe, depthframe, device.getdepthscale())
    if hands:
        cv2.drawContours(result, hands, -1, (0, 255, 0), 2)
        for p in points:
            cv2.circle(result, tuple(p), 2, (0, 0, 255))
    writer.write(result)
    await writer.drain()
    #cv2.namedWindow('RealSense', cv2.WND_PROP_FULLSCREEN)
    #cv2.setWindowProperty("RealSense", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    #cv2.imshow('Stream', recievedframe)
    #cv2.waitKey(1)
    writer.close()

async def start_client(ip):
    reader, writer = await asyncio.open_connection('localhost', 5555)
    data = await reader.read(-1)
    recievedframe = data.decode()
    #colorframe = device.getcolorstream()
    #depthframe = device.getdepthstream()
    #result, hands, points = hand.getHand(colorframe, depthframe, device.getdepthscale())
    #if hands:
    #    cv2.drawContours(result, hands, -1, (0, 255, 0), 2)
    #    for p in points:
    #        cv2.circle(result, tuple(p), 2, (0, 0, 255))
    #writer.write(result)
    #await writer.drain()
    cv2.namedWindow('RealSense', cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("RealSense", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow('Stream', recievedframe)
    cv2.waitKey(1)
    writer.close()

async def main():
    if (options.join):
            await asyncio.run(start_client(options.join))
    else:
        device = RealSense()
        server = await asyncio.start_server(handle_client, 'localhost', 5555)
        async with server:
            await server.serve_forever()

if __name__ == '__main__':
    asyncio.run(main())