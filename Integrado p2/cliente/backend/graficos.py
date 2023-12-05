import matplotlib as plt
from PyQt5.QtCore import QObject, pyqtSignal


class Datos(QObject):

    senal_datos = pyqtSignal(list)

    def __init__(self, parent, port, host):
