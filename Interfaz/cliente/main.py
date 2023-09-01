import json
import sys

from PyQt5.QtWidgets import QApplication
from frontend.ventana_interfaz import VentanaInterfaz
from backend.cliente import Cliente
from backend.logica import Logica


archivo_parametros = open("parametros.json", encoding="utf-8")#Abrimos archivo
PARAMETROS = json.load(archivo_parametros) # cargamos


class InterfazCliente(QApplication):
    """
    Aplicacion que permite conectar las senales de
    back y front de manera efectiva
    """
    def __init__(self, port, host, argv):
        super().__init__(argv)

        self.ventana = VentanaInterfaz()
        self.cliente = Cliente(port, host)
        self.logica = Logica()
        self.ventana.abrir()
        self.conectar_senales()
    
    def conectar_senales(self):
        
        # front -> logica
        self.ventana.senal_automatico.connect(self.logica.mandar_automatico)
        self.ventana.senal_manual.connect(self.logica.mandar_manual)
        self.ventana.senal_mensaje.connect(self.logica.mandar_mensaje_escrito)

        # logica -> cliente
        self.logica.senal_mensaje.connect(self.cliente.send)

        # cliente -> logica
        self.cliente.senal_mensaje.connect(self.logica.manejo_mensajes)

        # logica -> front
        self.logica.senal_modo_actual_recibido.connect(self.ventana.cambiar_texto_info)




if __name__ == '__main__':
    def hook(type_, value, traceback):
        print(type_)
        print(traceback)

    #port = int(sys.argv[1])
    port = 2020
    host = PARAMETROS["host"]

    sys.__excepthook__ = hook

    app = InterfazCliente(port, host, [])

    sys.exit(app.exec())