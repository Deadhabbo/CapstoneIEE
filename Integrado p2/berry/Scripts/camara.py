import cv2, imutils
from PyQt5.QtCore import QObject, pyqtSignal, QThread

WIDTH = 640

class Camara(QThread):

    senal_video = pyqtSignal(list)

    def __init__(self, parent):
        super().__init__(parent)
        self.video = cv2.VideoCapture(0)
    
    def run(self):
        while True:
            while self.video.isOpened():
                _,frame = self.video.read()
                frame = imutils.resize(frame, width=WIDTH)
                self.senal_video.emit([frame])
                