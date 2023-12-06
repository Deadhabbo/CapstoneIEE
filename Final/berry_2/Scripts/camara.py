import cv2, imutils, threading

WIDTH = 640

class Camara(threading.Thread):

    def __init__(self, serverUDP):
        super().__init__()
        self.video = cv2.VideoCapture(0)
        self.serverUDP = serverUDP
        self.procesador = None
    
    def run(self):
        while True:
            while self.video.isOpened():
                _,frame = self.video.read()
                self.frame = imutils.resize(frame, width=WIDTH)
                if self.procesador != None:
                    self.procesador.procesar()
                self.serverUDP.enviar(self.frame)
    
    def asignar_procesador(self, procesador):
        self.procesador = procesador
                