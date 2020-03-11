# import libraries
from classes.vidclient import VidClient
import cv2

#define netgear client with `receive_mode = True` and default settings
client = VidClient()

# infinite loop
while True:
    # receive frames from network
    frame = client.recieve()

    # check if frame is None
    if frame is None:
        #if True break the infinite loop
        break

    # do something with frame here

    # Show output window
    cv2.imshow("Output Frame", frame)

    key = cv2.waitKey(1) & 0xFF
    # check for 'q' key-press
    if key == ord("q"):
        #if 'q' key-pressed break out
        break

# close output window
cv2.destroyAllWindows()
# safely close client
client.close()