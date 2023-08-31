import json
import sys

from PyQt5.QtWidgets import QApplication
from frontend.ventana_interfaz import VentanaInterfaz


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
        self.ventana.abrir()
        self.conectar_senales()
    
    def conectar_senales(self):
        pass

if __name__ == '__main__':
    def hook(type_, value, traceback):
        print(type_)
        print(traceback)

    #port = int(sys.argv[1])
    port = 832
    host = PARAMETROS["host"]

    sys.__excepthook__ = hook

    app = InterfazCliente(port, host, [])

    sys.exit(app.exec())