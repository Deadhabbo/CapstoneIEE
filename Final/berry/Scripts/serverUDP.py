import typing
from PyQt5.QtCore import QObject, pyqtSignal, QThread
import cv2, imutils, socket
import numpy as np
import time
import base64
# https://pyshine.com/Send-video-over-UDP-socket-in-Python/

BUFF_SIZE = 921600


class ServerUDPThread(QThread):

    senal_direccion = pyqtSignal(tuple)
    senal_sock = pyqtSignal(list)

    def __init__(self, parent, port, host):
        super().__init__(parent)
        self.port = port
        self.host = host
        self.client_addr = None

    def run(self):

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
        self.server_socket.bind((self.host, self.port))
        self.senal_sock.emit([self.server_socket])
        while True:
            msg,client_addr = self.server_socket.recvfrom(BUFF_SIZE)
            self.client_addr = client_addr
            self.senal_direccion.emit(client_addr)
            print("Aquí llego si que si", msg)

        
class ServerUDP(QObject):

    def __init__(self, port, host) -> None:
        super().__init__()
        self.port = port
        self.host = host
        self.client_addr = None
        self.sock: socket = None

        self.hilo = ServerUDPThread(self, self.port, self.host)
        self.hilo.senal_direccion.connect(self.setear_cliente)
        self.hilo.senal_sock.connect(self.setear_sock)
        self.hilo.start()
    
    def enviar(self, frame_entrante):

        frame = frame_entrante[0]
        encoded,buffer = cv2.imencode('.jpg', frame,[cv2.IMWRITE_JPEG_QUALITY, 80])
        if self.client_addr != None:
            message = base64.b64encode(buffer)
            self.sock.sendto(message, self.client_addr)
        frame = cv2.putText(frame,'FPS: '+str(30),(10,40),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
        cv2.imshow('TRANSMITTING VIDEO',frame)
    
    def setear_cliente(self, direccion: tuple):
        self.client_addr = direccion
    
    def setear_sock(self, sock:list):
        self.sock: socket = sock[0]
        print(type(self.sock))


        



