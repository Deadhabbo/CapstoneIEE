import cv2, socket
import base64
import threading
# https://pyshine.com/Send-video-over-UDP-socket-in-Python/

BUFF_SIZE = 921600


class ServerUDP(threading.Thread):

    def __init__(self, port, host) -> None:
        super().__init__()
        self.daemon = True
        self.port = port
        self.host = host
        self.client_addr = None
        self.client_addr_lock = threading.Lock()  # Agrega un bloqueo

        self.server_socket: socket = None

    
    def run(self):

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
        self.server_socket.bind((self.host, self.port))
        while True:
            msg, client_addr = self.server_socket.recvfrom(BUFF_SIZE)
            with self.client_addr_lock:
                self.client_addr = client_addr
            print("Aquí llego si que si", msg)
    
    def enviar(self, frame_entrante):

        frame = frame_entrante
        encoded,buffer = cv2.imencode('.jpg', frame,[cv2.IMWRITE_JPEG_QUALITY, 80])
        with self.client_addr_lock:
            if self.client_addr != None:
                message = base64.b64encode(buffer)
                self.server_socket.sendto(message, self.client_addr)
        # frame = cv2.putText(frame,'FPS: '+str(30),(10,40),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
        # cv2.imshow('TRANSMITTING VIDEO',frame)
    
    def setear_cliente(self, direccion: tuple):
        self.client_addr = direccion


    def setear_sock(self, sock:list):
        self.sock: socket = sock[0]
        print(type(self.sock))





        



