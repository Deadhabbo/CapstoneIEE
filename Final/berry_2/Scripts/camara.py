import cv2, imutils, threading

WIDTH = 640

class Camara(threading.Thread):

    def __init__(self, serverUDP):
        super().__init__()
        self.video = cv2.VideoCapture(0)
        self.serverUDP = serverUDP
    
    def run(self):
        while True:
            while self.video.isOpened():
                _,frame = self.video.read()
                frame = imutils.resize(frame, width=WIDTH)
                self.serverUDP.enviar(frame)
                