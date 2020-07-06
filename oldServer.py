# import library
from vidgear.gears.asyncio import NetGear_Async
import cv2, asyncio

#initialize Server
server = NetGear_Async(address='0.tpc.ngrok.io', port='17854', logging = True)

#Create a async frame generator as custom source
async def my_frame_generator():

        #Open any video stream such as live webcam video stream on first index(i.e. 0) device
        stream = cv2.VideoCapture(0)

        # loop over stream until its terminated
        while True:

            # read frames
            (grabbed, frame) = stream.read()

            # check if frame empty
            if not grabbed:
                #if True break the infinite loop
                break

            # do something with the frame to be sent here

            # yield frame
            yield frame
            # sleep for sometime
            await asyncio.sleep(0.00001)


if __name__ == '__main__':
	#set event loop
	asyncio.set_event_loop(server.loop)
	#Add your custom source generator to Server configuration
	server.config["generator"] = my_frame_generator()
	#Launch the Server
	server.launch()
	try:
		#run your main function task until it is complete
		server.loop.run_until_complete(server.task)
	except KeyboardInterrupt:
		#wait for keyboard interrupt
		pass
	finally:
		# finally close the server
		server.close()