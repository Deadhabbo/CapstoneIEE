import json
from random import randint
import socket
from PyQt5.QtCore import QObject, pyqtSignal, QThread
import pickle

archivo_parametros = open("parametros.json", encoding="utf-8")#Abrimos archivo
PARAMETROS = json.load(archivo_parametros) # cargamos


class Server(QObject):

    def __init__(self, port, host):
        super().__init__()
        self.host = host
        self.port = port
        self.sockets = {}
        self.usuarios = {}
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
        address = address
        thread = listen_client_thread(self, socket_cliente)
        thread.senal_desconexion.connect(self.desconexion_usuario)
        thread.senal_desencriptado.connect(self.handle_command)
        self.threads_listen[socket_cliente] = thread
        thread.start()
    
    

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
        nombre = self.usuarios[client_socket]
        if recibido[0] == "Anunciar":
            self.juego.anunciar_valor_jugador(nombre, recibido[1])

        elif recibido[0] == "Pasar":
            self.juego.pasar_jugador(nombre)
        
        elif recibido[0] == "Cambiar Dados":
            self.juego.cambiar_dados_jugador(nombre)
        
        elif recibido[0] == "Poder":
            self.juego.usar_poder(nombre, recibido[1])
        
        elif recibido[0] == "Dudar":
            self.juego.dudar_jugador(nombre)

        elif recibido[0] == "Iniciar":
            self.juego.comenzar_partida()
        
        elif recibido[0] == "Recibido":
            pass

    def desconexion_usuario(self, sock: socket) -> None:
        """
        Si un cliente se desconectase informa en el log,
        se recupera su nombre y se elimina su socket
        """
        sock = sock[0]
        self.logs(self.usuarios[sock], "Desconectado", "-")
        nombre = self.usuarios[sock]
        self.usuarios_disponibles.append(nombre)
        del self.sockets[sock]
        del self.threads_listen[sock]
    
    # def proceso_aceptacion(self, socket_cliente, address):
    #     """
    #     Cuando un cliente se conecta al servidor se guardan sus datos
    #     y se le asigna un nombre
    #     """
    #     socket_cliente = socket_cliente[0]
    #     address = address
    #     self.sockets[socket_cliente] = address
    #     if len(self.usuarios_disponibles) > 0:
    #         aleatorio = randint(0, len(self.usuarios_disponibles) - 1)
    #         nombre = self.usuarios_disponibles.pop(aleatorio)
    #         self.usuarios[socket_cliente] = nombre
    #         thread = listen_client_thread(self, socket_cliente)
    #         thread.senal_desconexion.connect(self.desconexion_usuario)
    #         thread.senal_desencriptado.connect(self.handle_command)
    #         self.threads_listen[socket_cliente] = thread
    #         thread.start()
    #         self.logs(nombre, "Conectarse", "-")
    #         self.juego.agregar_jugador(Jugador(nombre))
    #         nombres = list(self.usuarios.values())
    #         mensaje = []
    #         for indice in range(len(nombres)):
    #             mensaje.append([indice, nombres[indice]])
    #         self.send(["Ventana Inicio", mensaje], socket_cliente)
    #     else:
    #         ##pasa si estamos llenos
    #         pass

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
            while len(mensaje) < largo_bytes_mensaje:
                read_length = min(4096, largo_bytes_mensaje - len(mensaje))
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


