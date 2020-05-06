# import required libraries
from vidgear.gears import NetGear
from vidgear.gears import VideoGear
import cv2

stream = VideoGear(source='C:\saest.mp4').start()

# activate bidirectional mode
options = {'bidirectional_mode': True}

#define Netgear Client with `receive_mode = True` and defined parameter
client = NetGear(receive_mode = True, pattern = 1, logging = True, **options)

# loop over
while True:

    try:
        # read frames from stream
        frame = stream.read()

        # check for frame if Nonetype
        if frame is None:
            break

        #prepare data to be sent


        # receive data from server and also send our data
        data = client.recv(return_data = frame)

        # check for data if None
        if data is None:
            break

        # extract server_data & frame from data
        # server_data, frame = data

        # again check for frame if None
        #if frame is None:
        #    break

        # {do something with the extracted frame and data here}

        # lets print extracted server data
        #if not(server_data is None):
        #    print(server_data)

        # Show output window
        cv2.imshow("Output Frame", data)

        # check for 'q' key if pressed
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

    except KeyboardInterrupt:
        break

# close output window
cv2.destroyAllWindows()

stream.close()

# safely close client
client.close()