from PyQt5.QtCore import QObject, pyqtSignal
from random import randint, choices, choice
import json


class Control(QObject):

    senal_modo_actual = pyqtSignal(list)

    def __init__(self, parent) -> None:
        super().__init__(parent)

        self._modo_actual = "Manual"
    
    @property
    def modo_actual(self) -> str:
        return self._modo_actual

    @modo_actual.setter
    def modo_actual(self, nuevo_valor: str) -> None:
        self._modo_actual = nuevo_valor
        self.senal_modo_actual.emit(["modo", self.modo_actual])
    
    def cambiar_modo(self, nuevo_valor: str) -> None:
        self.modo_actual = nuevo_valor
