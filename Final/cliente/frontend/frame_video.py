import typing
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (QWidget, QLabel, QPushButton, QFrame)
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QLineEdit
from PyQt5.QtGui import  QPixmap, QIcon, QFont, QImage
import json
from os.path import join

class CuadroVideo(QLabel, QFrame):

    senal_click = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 480,360)
        self.setFixedSize(480, 360)
        self.setStyleSheet("background-color:black")

    
    def cambiar_frame(self, frame) -> None:
        self.setPixmap(QPixmap.fromImage(frame))
        self.show()
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.pressPos_izq = event.pos()
            self.x_izq = self.pressPos_izq.x()
            self.y_izq = self.pressPos_izq.y()
            print("izquierdo", self.x_izq , self.y_izq)
            self.senal_click.emit(["Izquierdo", self.x_izq , self.y_izq ])

        elif event.button() == Qt.RightButton:
            self.pressPos_der = event.pos()
            self.x_der = self.pressPos_der.x()
            self.y_der = self.pressPos_der.y()
            print("derecho", self.x_der ,self.y_der)
            self.senal_click.emit(["Derecho", self.x_der , self.y_der ])



