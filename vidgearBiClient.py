# import required libraries
from vidgear.gears import NetGear
from vidgear.gears import VideoGear
from classes.realsense import RealSense
import base64
import cv2
import numpy as np

from PIL import Image
import skimage
import skimage.io
import base64
from io import BytesIO
import json

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

def encode(image) -> str:

    # convert image to bytes
    with BytesIO() as output_bytes:
        PIL_image = Image.fromarray(skimage.img_as_ubyte(image))
        PIL_image.save(output_bytes, 'JPEG') # Note JPG is not a vaild type here
        bytes_data = output_bytes.getvalue()

    # encode bytes to base64 string
    base64_str = str(base64.b64encode(bytes_data), 'utf-8')
    return base64_str

def decode(base64_string):
    if isinstance(base64_string, bytes):
        base64_string = base64_string.decode("utf-8")

    imgdata = base64.b64decode(base64_string)
    img = skimage.io.imread(imgdata, plugin='imageio')
    return img

# open any valid video stream(for e.g `test.mp4` file)
#stream = VideoGear(source='C:\saest.mp4').start()
device = RealSense("752112070399")

# activate bidirectional mode
options = {'bidirectional_mode': True}

# define Netgear Client with `receive_mode = True` and defined parameter
# client = NetGear(receive_mode=True, pattern=1, logging=True, **options) local
client = NetGear(address = '192.168.0.31', port = '5454', protocol = 'tcp',  pattern = 1, receive_mode = True, logging = True, **options)

# loop over
while True:

    # prepare data to be sent
    # target_data = "Hi, I am a Client here."

    # read frames from stream
    # frame = stream.read()
    frame = device.getcolorstream()

    # check for frame if Nonetype
    if frame is None:
        break

    # retval, buffer = cv2.imencode('.jpg', frame)
    # target_data = base64.b64encode(buffer)
    # target_data = base64.b64encode(frame)
    # target_data = frame
    #base64_bytes = base64.b64encode(frame)
    #base64_string = base64_bytes.decode('utf-8')
    #target_data = base64_string
    # print(frame)

    target_data = encode(frame)
    #decoded_data = decode(target_data)
    #cv2.imshow("Server frame, displayed on the Client machine", decoded_data)
    # print(img_encoded)
    #target_data = img_encoded.tostring()
    #target_data = img_encoded


    # receive data from server and also send our data
    data = client.recv(return_data=target_data)

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
    if not (server_data is None):
        print(server_data)

    # Show output window
    cv2.imshow("Server frame, displayed on the Client machine", frame)

    # check for 'q' key if pressed
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

# close output window
cv2.destroyAllWindows()

device.stop()

# safely close client
client.close()
