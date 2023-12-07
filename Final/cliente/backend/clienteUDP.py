import cv2, imutils, socket
from PyQt5.QtCore import QObject, pyqtSignal, QThread
import numpy as np
import time
import base64
from PyQt5.QtGui import QImage
from PyQt5.QtCore import Qt 
# https://pyshine.com/Send-video-over-UDP-socket-in-Python/

BUFF_SIZE = 921600

class ClienteUDP(QThread):

    senal_frame = pyqtSignal(QImage)

    def __init__(self, parent, port, host):
        super().__init__(parent)
        self.host = host
        self.port = port
        self.frames_to_count = 20
        self.fps = 0
        self.cnt = 0
        self.st = 0
    
    def run(self) -> None:
        self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket_client.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
        print("inicio RUN Thread UDP")
        mensaje = b'Conexion UDP'
        print("mensaje a enviar", mensaje)
        self.socket_client.sendto(mensaje,(self.host, self.port))
        while True:
            packet,_ = self.socket_client.recvfrom(BUFF_SIZE)
            data = base64.b64decode(packet,' /')
            npdata = np.frombuffer(data,dtype=np.uint8)
            frame = cv2.imdecode(npdata,1)
            imagen = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.putText(frame,'FPS: '+str(self.fps),(10,40),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
            #cv2.imshow("RECEIVING VIDEO",frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                self.client_socket.close()
                break
            if self.cnt == self.frames_to_count:
                try:
                    self.fps = round(self.frames_to_count/(time.time()-self.st))
                    self.st=time.time()
                    self.cnt=0
                except:
                    pass
            self.cnt+=1


            
            
            imagen = QImage(imagen.data, imagen.shape[1], imagen.shape[0], QImage.Format_RGB888)
            self.senal_frame.emit(imagen)



