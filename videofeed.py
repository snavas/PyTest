import cv2
from PIL import Image

class VideoFeed:

    def __init__(self,mode=1,name="w1",capture=1):
        print(name)
        if mode == 1:
            cv2.StartWindowThread()
            cv2.NamedWindow(name, cv2.CV_WINDOW_AUTOSIZE)
        self.camera_index = 0
        self.name=name
        if capture == 1:
            self.capture = cv2.CaptureFromCAM(self.camera_index)

    def get_frame(self):
        self.frame = cv2.QueryFrame(self.capture)
        self.c = cv2.WaitKey(1)
        if(self.c=="n"): #in "n" key is pressed while the popup window is in focus
            self.camera_index += 1 #try the next camera index
            self.capture = cv2.CaptureFromCAM(self.camera_index)
            if not self.capture: #if the next camera index didn't work, reset to 0.
                self.camera_index = 0
                self.capture = cv2.CaptureFromCAM(self.camera_index)
        jpegImg= Image.fromstring("RGB",cv2.GetSize(self.frame),self.frame.tostring())
        retStr=jpegImg.tostring("jpeg","RGB")
        print("Compressed Size = ",len(retStr))
        return retStr

#jpeg.compress(self.frame,640,480,8)

    def set_frame(self, frame):
#im image("RGB",(640,480))
        jpegPIL = Image.fromstring("RGB",(640,480),frame,"jpeg","RGB","raw")
        cv_im = cv2.CreateImage((640,480), cv2.IPL_DEPTH_8U, 3)
        cv2.SetData(cv_im,jpegPIL.tostring())
        cv2.ShowImage(self.name, cv_im)
if __name__=="__main__":
    vf = VideoFeed(1,"test",1)
    while 1:
        m = vf.get_frame()
        vf.set_frame(m)
       
