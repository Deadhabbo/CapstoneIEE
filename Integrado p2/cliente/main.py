import json
import sys

from PyQt5.QtWidgets import QApplication
from frontend.ventana_interfaz import VentanaInterfaz
from backend.clienteTCP import ClienteTCP
from backend.logica import Logica
from backend.clienteUDP import ClienteUDP

archivo_parametros = open("parametros.json", encoding="utf-8")#Abrimos archivo
PARAMETROS = json.load(archivo_parametros) # cargamos


class InterfazCliente(QApplication):
    """
    Aplicacion que permite conectar las senales de
    back y front de manera efectiva
    """
    def __init__(self, tcpport, udpport, host, argv):
        super().__init__(argv)

        self.ventana = VentanaInterfaz()
        self.clienteUDP = ClienteUDP(self, udpport, host)
        self.logica = Logica()
        self.clienteTCP = ClienteTCP(tcpport, host)
        

        
        
        self.conectar_senales()
        self.ventana.abrir()
        
    def conectar_senales(self):

        
        
        # front -> logica
        self.ventana.senal_automatico.connect(self.logica.mandar_automatico)
        self.ventana.senal_manual.connect(self.logica.mandar_manual)
        self.ventana.senal_mensaje.connect(self.logica.mandar_mensaje_escrito)

        # logica -> cliente
        self.logica.senal_mensaje.connect(self.clienteTCP.send)

        # clienteTCP -> logica
        self.clienteTCP.senal_mensaje.connect(self.logica.manejo_mensajes_tcp)

        # clienteUDP -> front
        self.clienteUDP.senal_frame.connect(self.ventana.cambiar_frame_video)

        # logica -> front
        self.logica.senal_modo_actual_recibido.connect(self.ventana.cambiar_texto_info)


        self.clienteUDP.start()



if __name__ == '__main__':
    
    def hook(type_, value, traceback):
        print(type_)
        print(traceback)

    #port = int(sys.argv[1])
    tcp_port = 2020
    udp_port = 9999
    host = PARAMETROS["host"]

    sys.__excepthook__ = hook

    app = InterfazCliente(tcp_port, udp_port, host, [])

    sys.exit(app.exec())