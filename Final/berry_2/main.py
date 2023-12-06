import sys
import json
from Scripts.serverTCP import ServerTCP
from Scripts.serverUDP import ServerUDP
from Scripts.control import Control
from Scripts.camara import Camara
from Scripts.procesado import Procesado
#from Scripts.camara_v3 import PiCamera
import threading

archivo_parametros = open("parametros.json", encoding="utf-8")
PARAMETROS = json.load(archivo_parametros)

class HiloPrincipal(threading.Thread):

    def __init__(self, tcpport, udpport, host):
        super().__init__(name="Principal")
        self.daemon = False
        self.udpport = udpport
        self.tcpport = tcpport
        self.host = host

        self.control = Control()

    def run(self):
        try:
            
            self.serverTCP = ServerTCP(self.tcpport, self.host, self.control)
            self.serverUDP = ServerUDP(self.udpport, self.host)
            self.camara = Camara(self.serverUDP)
            self.procesado = Procesado(self.camara)
            self.camara.procesador = self.procesado
            
            self.serverTCP.asignar_procesador(self.procesado)
            # Iniciar los hilos
            self.serverUDP.start()
            self.camara.start()

            # Esperar a que los hilos terminen
            self.serverUDP.join()
            self.camara.join()

        except KeyboardInterrupt:
            print("Finalizado")


if __name__ == '__main__':
    def hook(type_, value, traceback):
        print(type_)
        print(traceback)
    
    tcp_port = 2020
    udp_port = 9999
    host = PARAMETROS["host"]

    sys.__excepthook__ = hook

    principal = HiloPrincipal(tcp_port, udp_port, host)
    principal.start()
    principal.join()  # Esperar a que HiloPrincipal termine antes de salir