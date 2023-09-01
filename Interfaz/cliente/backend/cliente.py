import socket
from PyQt5.QtCore import QObject, pyqtSignal, QThread
import pickle
from sys import exit


class Cliente(QObject):
    """
    Maneja toda la comunicación desde el lado del cliente.
    """
    senal_mensaje = pyqtSignal(list)
    def __init__(self, port, host):
        super().__init__()
        self.host = host
        self.port = port
        self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.hilo = None
        try:
            self.connect_to_server()
            self.listen()
        except ConnectionError:
            print("Conexión terminada.")
            self.socket_client.close()
            exit()

    def connect_to_server(self):
        """Crea la conexión al servidor."""
        self.socket_client.connect((self.host, self.port))

    def listen(self):
        """
        Inicializa el thread que escuchará los mensajes del servidor.

        Es útil hacer un thread diferente para escuchar al servidor,
        ya que de esa forma podremos tener comunicación asíncrona con este.
        Luego, el servidor nos podrá enviar mensajes sin necesidad de
        iniciar una solicitud desde el lado del cliente.

        
        """
        thread = listen_thread(self, self.socket_client)
        thread.senal_desencriptado.connect(self.salto_mensaje)
        thread.start()
    
    def salto_mensaje(self, mensaje: list):
        """
        Enviamos senal del mensaje
        """
        self.senal_mensaje.emit(mensaje)

    def send(self, msg: list):
        """
        Envía mensajes al servidor.
        """
        msg_dumpeado = pickle.dumps(msg) # pasamos a pickle
        largo = len(msg_dumpeado) # Obtenemos largo mensaje
        largo_bytes = largo.to_bytes(4, byteorder = "little") # pasamos largo a bytes
        mensaje = bytearray() # mensaje en bytes a enviar
        mensaje.extend(largo_bytes + msg_dumpeado) # agregamos largo de mensaje
        self.socket_client.sendall(mensaje) #mandamos el mensaje completo




class listen_thread(QThread):
    """
    Hilo que se encargara de escuchar al server
    """
    senal_desencriptado = pyqtSignal(list)
    def __init__(self, parent, sock) -> None:
        super().__init__(parent)
        self.sock: socket = sock

    def run(self) -> None:
        """
        Siempre se intenta recibir bytes desde el server para
        saber el largo del mensaje a recibir
        """
        while True:
            try:
                largo_bytes_mensaje = self.sock.recv(4)
                largo_mensaje = int.from_bytes(
                                largo_bytes_mensaje, byteorder='little')
                
                mensaje = bytearray()
            except Exception as e: # si falla cerramos conexion
                    print("Error", e)
                    self.senal_desencriptado.emit(["Fin server"])
                    print("Server desconectado")
                    break
            # Recibimos datos hasta que alcancemos la totalidad de los datos
            # indicados en los primeros 4 bytes recibidos.
            while len(mensaje) < largo_mensaje:
                read_length = min(4096, largo_mensaje - len(mensaje))
                mensaje.extend(self.sock.recv(read_length))

            desencriptado_util = pickle.loads(mensaje)
            print(desencriptado_util)
            self.senal_desencriptado.emit(desencriptado_util) # Emitimos senal 


