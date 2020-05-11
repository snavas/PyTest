# import library
from vidgear.gears.asyncio import NetGear_Async
from classes.realsense import RealSense
import libs.hand as hand
import libs.draw as draw
import numpy as np
import cv2, asyncio

# Create a async frame generator as custom source
async def custom_frame_generator():
    # Open video stream
    device = RealSense("752112070399")
    # loop over stream until its terminated
    while True:
        # read frames
        frame = device.getcolorstream()
        # check if frame empty
        if frame is None:
            break
        # yield frame
        yield frame
        # sleep for sometime
        await asyncio.sleep(0.01)
    # close stream
    device.stop()

# Create a async function where you want to show/manipulate your received frames
async def client_iterator(client):
    # loop over Client's Asynchronous Frame Generator
    async for frame in client.recv_generator():
        # do something with received frames here

        # Show output window
        cv2.imshow("Output Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        # await before continuing
        await asyncio.sleep(0.00001)

async def netgear_async_playback(pattern):
    try:
        # define and launch Client with `receive_mode = True`
        client = NetGear_Async(
            port = 6666, logging=True, pattern=pattern, receive_mode=True
        ).launch()
        server = NetGear_Async(
            address = '192.168.0.31', port = 5555, pattern=pattern, logging=True
        )
        server.config["generator"] = custom_frame_generator()
        server.launch()
        # gather and run tasks
        input_coroutines = [server.task, client_iterator(client)]
        res = await asyncio.gather(*input_coroutines, return_exceptions=True)
    except Exception as e:
        #pytest.fail(str(e))
        pass
    finally:
        server.close(skip_loop=True)
        client.close(skip_loop=True)




# Create a async function where you want to show/manipulate your received frames
async def main():
    # loop over Client's Asynchronous Frame Generator
    async for frame in client.recv_generator():
        # do something with received frames here

        # Show output window
        cv2.imshow("Output Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        # await before continuing
        await asyncio.sleep(0.00001)


# Create a async frame generator as custom source
async def my_frame_generator():
    # Open any video stream such as live webcam video stream on first index(i.e. 0) device


    # loop over stream until its terminated
    while True:

        # read frames
        colorframe = device.getcolorstream()
        depthframe = device.getdepthstream()

        # check if frame empty
        if colorframe is None:
            # if True break the infinite loop
            break

        # do something with the frame to be sent here
        result, hands, points = hand.getHand(colorframe, depthframe, device.getdepthscale())
        if hands:
            cv2.drawContours(result, hands, -1, (0, 255, 0), 2)
            for p in points:
                cv2.circle(result, tuple(p), 2, (0, 0, 255))
        drawings = draw.getDraw(colorframe)

        # yield frame
        #yield cv2.bitwise_or(result, drawings)
        yield colorframe
        # sleep for sometime
        await asyncio.sleep(0.00001)


if __name__ == '__main__':
    asyncio.run(netgear_async_playback(1))