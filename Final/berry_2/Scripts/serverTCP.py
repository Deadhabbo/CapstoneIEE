import socket
import threading
import pickle
import json

archivo_parametros = open("parametros.json", encoding="utf-8")#Abrimos archivo
PARAMETROS = json.load(archivo_parametros) # cargamos

class ServerTCP:
    def __init__(self, port, host, control):
        print("Inicializando servidor...")
        self.host = host
        self.port = port
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.control = control
        self.bind_and_listen()
        self.accept_connections()
    

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
        print(f"Servidor escuchando en {self.host}:{self.port}...")

    def accept_connections(self):
        """
        Inicia el thread que aceptará clientes.

        Aunque podríamos aceptar clientes en el thread principal de la
        instancia, es útil hacerlo en un thread aparte. Esto nos
        permitirá realizar la lógica en la parte del servidor sin dejar
        de aceptar clientes. Por ejemplo, seguir procesando archivos.
        """
        thread = threading.Thread(target=self.accept_connections_thread)
        thread.start()

    def accept_connections_thread(self):
        """
        Es arrancado como thread para aceptar clientes.

        Cada vez que aceptamos un nuevo cliente, iniciamos un
        thread nuevo encargado de manejar el socket para ese cliente.
        """
        print("Servidor aceptando conexiones...")

        while True:
            client_socket, _ = self.socket_server.accept()
            listening_client_thread = threading.Thread(
                target=self.listen_client_thread,
                args=(client_socket, ),
                daemon=True)
            listening_client_thread.start()

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


    def listen_client_thread(self, client_socket):
        """
        Es ejecutado como thread que escuchará a un cliente en particular.

        Implementa las funcionalidades del protocolo de comunicación
        que permiten recuperar la informacion enviada.
        """
        print("Servidor conectado a un nuevo cliente...")

        while True:
            while True:
                try: # intentamos leer mensaje
                    largo_bytes_mensaje = client_socket.recv(4) # los 4 bytes del largo
                    largo_mensaje = int.from_bytes(
                                    largo_bytes_mensaje, byteorder='little')
                    mensaje = bytearray() #Comenzamos bytearray
                except Exception as e:
                        """
                        Si un cliente se desconecta se termina el hilo
                        """
                        self.desconexion_usuario()
                        break
                while len(mensaje) < largo_mensaje:
                    read_length = min(4096, largo_mensaje - len(mensaje))
                    mensaje.extend(client_socket.recv(read_length))
                # cargamos
                cargado = pickle.loads(mensaje)
                print("Se recibe/cargado", cargado)
                if cargado != "":
                    # El método `self.handle_command()` debe ser definido.
                    # Este realizará toda la lógica asociado a los mensajes
                    # que llegan al servidor desde un cliente en particular.
                    # Se espera que retorne la respuesta que el servidor
                    # debe enviar hacia el cliente.
                    response = self.handle_command(cargado, client_socket)
                    self.send(response, client_socket)

    def handle_command(self, recibido, client_socket):
        """
        Cada mensaje recibido desde los clientes es procesado
        desde aqui, donde dependiendo del comando recibido
        se procede con una u otra accion
        """
        print("Se recibe", recibido)
        comando = recibido[0]
        contenido = recibido[1]

        if comando == "modo":
            self.control.cambiar_modo(contenido)
            mensaje = ["modo", self.control.modo_actual]
            self.send(mensaje, client_socket)

        elif comando == "escrito":
            print("Ha llegado el mensaje:", contenido)
        
        elif comando == "pixel":
            print("Ha llegado el pixel", contenido)
            self.procesador.calibrate_color(contenido[0] , contenido[1], contenido[2])
    
    def asignar_procesador(self, procesador):
        self.procesador = procesador
    
    def desconexion_usuario(self) -> None:
        """
        Si un cliente se desconectase informa en el log
        y se elimina su socket
        """
        pass