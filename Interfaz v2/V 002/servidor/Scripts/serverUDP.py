from PyQt5.QtCore import QObject, pyqtSignal, QThread
import cv2, imutils, socket
import numpy as np
import time
import base64
# https://pyshine.com/Send-video-over-UDP-socket-in-Python/

BUFF_SIZE = 65536
WIDTH=400

class ServerUDP(QObject):

    def __init__(self, port, host):
        super().__init__()
        self.port = port
        self.host = host
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
        self.server_socket.bind((self.host, self.port))
        self.client_addr = None
        
    
    def pre_send(self, frame_entrante):

        frame = imutils.resize(frame_entrante, width = WIDTH)
        encoded,buffer = cv2.imencode('.jpg', frame,[cv2.IMWRITE_JPEG_QUALITY, 80])
        message = base64.b64encode(buffer)
        self.send(message)
    
    def send(self, frame_encoded):

        self.server_socket.sendto(frame_encoded, self.client_addr)

    def setear_direccion_cliente(self, direccion: tuple):

        self.client_addr = direccion[0]
        print(self.client_addr)

