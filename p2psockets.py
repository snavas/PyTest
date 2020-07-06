import socket, select, time
from classes.realsense import RealSense
import libs.hand as hand
import libs.draw as draw
import cv2

s = socket.socket()
s.setblocking(0)
s.bind((socket.gethostname(), 8080))
s.listen(10)

connections = [s]

device = RealSense("752112070399")

while True:
    try:
        time.sleep(.1)

        recv,write,err = select.select(connections,connections,connections)

        for socket in recv:
            if socket == s:
                client,address = socket.accept()
                connections.append(client)
            else:
                frame = socket.recv()
                #print("Recieved message from a socket, message was: "+str(msg))
                cv2.imshow("Output Frame", frame)

        for socket in write:
            #socket.send(bytes("Hi", "UTF-8"))
            colorframe = device.getcolorstream()
            socket.send(colorframe)

        for socket in err:
            print("Error with a socket")
            socket.close()
            connections.remove(socket)

    except KeyboardInterrupt:
        # wait for keyboard interrupt
        pass

    finally:
        # finally close the server
        cv2.destroyAllWindows()
        device.close()
        for c in connections:
            c.close()