# import required libraries
from vidgear.gears import NetGear
import cv2

# activate bidirectional mode
options = {'bidirectional_mode': True}

#define Netgear Client with `receive_mode = True` and defined parameter
client = NetGear(receive_mode = True, pattern = 1, logging = True, **options)

# loop over
while True:

    #prepare data to be sent
    target_data = "Hi, I am a Client here."

    # receive data from server and also send our data
    data = client.recv(return_data = target_data)

    # check for data if None
    if data is None:
        break

    # extract server_data & frame from data
    server_data, frame = data

    # again check for frame if None
    if frame is None:
        break

    # {do something with the extracted frame and data here}

    # lets print extracted server data
    if not(server_data is None):
        print(server_data)

    # Show output window
    cv2.imshow("Output Frame", frame)

    # check for 'q' key if pressed
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

# close output window
cv2.destroyAllWindows()

# safely close client
client.close()