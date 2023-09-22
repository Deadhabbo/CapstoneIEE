import sys
import json

from Scripts.serverTCP import ServerTCP
from Scripts.serverUDP import ServerUDP
from Scripts.control import Control
from PyQt5.QtWidgets import QApplication

archivo_parametros = open("parametros.json", encoding="utf-8")#Abrimos archivo
PARAMETROS = json.load(archivo_parametros) # cargamos

"""
Creamos una aplicación para mantener el server
activo con sus valores
"""
class ServidorInterfaz(QApplication):
    
    def __init__(self, tcpport, udpport, host, argv):
        super().__init__(argv)
        self.serverTCP = ServerTCP(tcpport, host)
        self.control = Control(self)
        self.serverUDP = ServerUDP(udpport, host)


        self.control.senal_modo_actual.connect(self.serverTCP.mandar)
        self.serverTCP.senal_cambio_modo.connect(self.control.cambiar_modo)
        self.serverTCP.senal_addres_cliente.connect(self.serverUDP.setear_direccion_cliente)

if __name__ == '__main__':
    def hook(type_, value, traceback):
        print(type_)
        print(traceback)

    #port = int(sys.argv[1])
    tcp_port = 2020
    udp_port = 9999
    host = PARAMETROS["host"] # Asignamos ip host

    sys.__excepthook__ = hook

    app = ServidorInterfaz(tcp_port, udp_port, host, []) # iniciamos servidor

    sys.exit(app.exec()) 