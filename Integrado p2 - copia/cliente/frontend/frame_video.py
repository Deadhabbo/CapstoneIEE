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
        self.setGeometry(0, 0, 640, 480)
        self.setFixedSize(640, 480)
        self.setStyleSheet("background-color:black")

    
    def cambiar_frame(self, frame) -> None:
        self.setPixmap(QPixmap.fromImage(frame))
        self.show()


