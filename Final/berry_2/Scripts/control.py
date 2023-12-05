import json, threading


class Control:

    def __init__(self) -> None:

        self._modo_actual = "Manual"
    
    @property
    def modo_actual(self) -> str:
        return self._modo_actual

    @modo_actual.setter
    def modo_actual(self, nuevo_valor: str) -> None:
        self._modo_actual = nuevo_valor
    
    def cambiar_modo(self, nuevo_valor: str) -> None:
        self.modo_actual = nuevo_valor
