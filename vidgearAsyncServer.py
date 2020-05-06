# import library
from vidgear.gears.asyncio import NetGear_Async
from classes.realsense import RealSense
import libs.hand as hand
import libs.draw as draw
import cv2, asyncio

# initialize Server
server = NetGear_Async(logging=True)

# define and launch Client with `receive_mode = True`
client = NetGear_Async(receive_mode=True).launch()

device = RealSense("752112070399")

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
    # set event loop
    asyncio.set_event_loop(server.loop)
    asyncio.set_event_loop(client.loop)
    # Add your custom source generator to Server configuration
    server.config["generator"] = my_frame_generator()
    # Launch the Server
    server.launch()
    try:
        # run your main function task until it is complete
        server.loop.run_until_complete(server.task)
        client.loop.run_until_complete(main())
    except KeyboardInterrupt:
        # wait for keyboard interrupt
        pass
    finally:
        # finally close the server
        cv2.destroyAllWindows()
        device.close()
        server.close()
        client.close()