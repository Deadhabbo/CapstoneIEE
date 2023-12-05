import json
import socket
from PyQt5.QtCore import QObject, pyqtSignal, QThread
import pickle

archivo_parametros = open("parametros.json", encoding="utf-8")#Abrimos archivo
PARAMETROS = json.load(archivo_parametros) # cargamos


class ServerTCP(QObject):

    senal_cambio_modo = pyqtSignal(str)


    def __init__(self, port, host):
        super().__init__()
        self.host = host
        self.port = port
        self.sockets = {}
        self.threads_listen = {}
        
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.bind_and_listen()
        self.accept_connections()
        self.log_inicial()
        self.logs("-", "Iniciando", "Server iniciado")
        

    def log_inicial(self) -> None:
        pass

    def logs(self, cliente, evento, descripcion):
        linea = [cliente, "|", evento, "|" , descripcion]
        fila_formato = "{:<30} {:<3} {:<30} {:<3} {:<30}"
        print(fila_formato.format(*linea))
        entre_linea = ["-"*30, "|", "-"*30, "|" ,"-"*30]
        print(fila_formato.format(*entre_linea))

    def bind_and_listen(self):
        """
        Enlaza el socket creado con el host y puerto indicado.

        Primero, se enlaza el socket y luego queda esperando
        por conexiones entrantes.
        """
        self.socket_server.bind((self.host, self.port))
        self.socket_server.listen()

    def accept_connections(self):
        """
        Inicia el Qthread que aceptará clientes.
        """
        thread = aceptar_conexiones_thread(self, self.socket_server)
        thread.senal_aceptado.connect(self.escuchar)
        thread.start()
    
    def escuchar(self, socket_cliente, address):
        socket_cliente = socket_cliente[0]
        self.sockets[socket_cliente] = address
        address = address
        thread = listen_client_thread(self, socket_cliente)
        thread.senal_desconexion.connect(self.desconexion_usuario)
        thread.senal_desencriptado.connect(self.handle_command)
        self.threads_listen[socket_cliente] = thread
        thread.start()
    
    
    def mandar(self, mensaje):
        sock = list(self.sockets.keys())
        sock = sock[0]
        self.send(mensaje, sock)

    @staticmethod
    def send(mensaje, sock):
        """
        Envía mensajes hacia algún socket cliente.
        """
        msg_dumpeado = pickle.dumps(mensaje) # pasamos a pickle
        largo = len(msg_dumpeado) # Obtenemos largo mensaje
        largo_bytes = largo.to_bytes(4, byteorder = "little") # pasamos largo a bytes
        mensaje = bytearray() # mensaje en bytes a enviar
        mensaje.extend(largo_bytes + msg_dumpeado) # agregamos largo de mensaje
        sock.sendall(mensaje) # mandamos todo el mensaje

    def handle_command(self, recibido, client_socket):
        """
        Cada mensaje recibido desde los clientes es procesado
        desde aqui, donde dependiendo del comando recibido
        se procede con una u otra accion
        """
        print("Se recibe", recibido)
        client_socket = client_socket[0]
        comando = recibido[0]
        contenido = recibido[1]

        if comando == "modo":
            self.senal_cambio_modo.emit(contenido)

        elif comando == "escrito":
            print("Ha llegado el mensaje:", contenido)

        
        

    def desconexion_usuario(self, sock: socket) -> None:
        """
        Si un cliente se desconectase informa en el log
        y se elimina su socket
        """
        sock = sock[0]
        self.logs("-", "Desconectado", "-")
        del self.sockets[sock]
        del self.threads_listen[sock]
    
"""
Comienzo de las clases que permiten ejecutar los
threads
"""


class listen_client_thread(QThread):
    senal_desencriptado = pyqtSignal(list, list) #mensaje [sock[]
    senal_desconexion = pyqtSignal(list) #  [sock]

    def __init__(self, parent, sock) -> None:
        super().__init__(parent)
        self.sock: socket = sock
    
    def run(self) -> None: # Ejecucion del qthread
        while True:
            try: # intentamos leer mensaje
                largo_bytes_mensaje = self.sock.recv(4) # los 4 bytes del largo
                largo_mensaje = int.from_bytes(
                                largo_bytes_mensaje, byteorder='little')
                mensaje = bytearray() #Comenzamos bytearray
            except Exception as e:
                    """
                    Si un cliente se desconecta se termina el hilo
                    """
                    socket_guardado = [self.sock]
                    self.senal_desconexion.emit(socket_guardado)
                    break
            while len(mensaje) < largo_mensaje:
                read_length = min(4096, largo_mensaje - len(mensaje))
                mensaje.extend(self.sock.recv(read_length))
            # cargamos
            cargado = pickle.loads(mensaje)
            socket_guardado = [self.sock]
            self.senal_desencriptado.emit(cargado, socket_guardado)
            # Emitimos senal del mensje recibido

class aceptar_conexiones_thread(QThread):

    senal_aceptado = pyqtSignal(list, tuple) # [sock] (addres)

    def __init__(self, parent, sock) -> None:
        super().__init__(parent)
        self.sock: socket = sock
    
    def run(self) -> None:

        while True:
            socket_cliente, address = self.sock.accept() #aceptamos conexion
            socket_guardado = [socket_cliente] # dejamos socket en lista para enviarlo
            # Esto lo hacemos ya que simplifica el uso de la senal
            self.senal_aceptado.emit(socket_guardado, address) #emitimos


