import cv2, imutils, socket
from PyQt5.QtCore import QObject, pyqtSignal, QThread
import numpy as np
import time
import base64

# https://pyshine.com/Send-video-over-UDP-socket-in-Python/

BUFF_SIZE = 65536

class ClienteUDP(QObject):

    senal_mensaje = pyqtSignal(list)

    def __init__(self, port, host):
        super().__init__()
        self.host = host
        self.port = port
        self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket_client.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
    
    def listen(self):

        thread = ListenThreadUDP(self, self.socket_client)
        thread.senal_frame.connect(self.salto_mensaje)
        thread.start()

    def salto_mensaje(self, mensaje: list):
        """
        Enviamos senal del mensaje
        """
        self.senal_mensaje.emit(mensaje)


class ListenThreadUDP(QThread):

    senal_frame = pyqtSignal(list)

    def __init__(self, parent, sock) -> None:
        super().__init__(parent)
        self.sock: socket = sock
    
    def run(self) -> None:

        while True:
            packet,_ = self.sock.recvfrom(BUFF_SIZE)
            data = base64.b64decode(packet,' /')
            npdata = np.frombuffer(data,dtype=np.uint8)
            frame = cv2.imdecode(npdata,1)
            self.senal_frame.emit([frame])
