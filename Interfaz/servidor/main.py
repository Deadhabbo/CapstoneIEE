import sys
import json

from Scripts.server import Server
from Scripts.control import Control
from PyQt5.QtWidgets import QApplication

archivo_parametros = open("parametros.json", encoding="utf-8")#Abrimos archivo
PARAMETROS = json.load(archivo_parametros) # cargamos

"""
Creamos una aplicación para mantener el server
activo con sus valores
"""
class ServidorInterfaz(QApplication):
    
    def __init__(self, port, host, argv):
        super().__init__(argv)
        self.server = Server(port, host)
        self.control = Control(self)


        self.control.senal_modo_actual.connect(self.server.mandar)
        self.server.senal_cambio_modo.connect(self.control.cambiar_modo)


if __name__ == '__main__':
    def hook(type_, value, traceback):
        print(type_)
        print(traceback)

    #port = int(sys.argv[1])
    port = 832
    host = PARAMETROS["host"] # Asignamos ip host

    sys.__excepthook__ = hook

    app = ServidorInterfaz(port, host, []) # iniciamos servidor

    sys.exit(app.exec()) 