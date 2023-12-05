import sys
import json

from Scripts.serverTCP import ServerTCP
from Scripts.serverUDP import ServerUDP
from Scripts.control import Control
#from Scripts.camara_v2 import Camara
from Scripts.camara import Camara
import threading

archivo_parametros = open("parametros.json", encoding="utf-8")#Abrimos archivo
PARAMETROS = json.load(archivo_parametros) # cargamos

class HiloPrincipal(threading.Thread):

    def __init__(self, tcpport, udpport, host):
        super().__init__(name="Principal")
        self.daemon = False
        self.udpport  = udpport
        self.tcpport  = tcpport
        self.host = host

        self.control = Control()

        self.serverTCP = ServerTCP(tcpport, host)
        self.serverUDP = ServerUDP(udpport, host)

        self.camara = Camara(self.serverUDP)
        
        
    def run(self):
        
        try:
            self.camara.start()
            while True:
                pass
        except KeyboardInterrupt:
            print("Finalizado")


if __name__ == '__main__':

    def hook(type_, value, traceback):
        print(type_)
        print(traceback)
    
    tcp_port = 2020
    udp_port = 9999
    host = PARAMETROS["host"] # Asignamos ip host

    sys.__excepthook__ = hook

    principal = HiloPrincipal(tcp_port, udp_port, host)

    principal.start()
        
    