import typing
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (QWidget, QLabel, QPushButton, QComboBox)
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QLineEdit
from PyQt5.QtGui import  QPixmap, QIcon, QFont, QImage
import json
from os.path import join

from frontend.frame_video import CuadroVideo

archivo_parametros = open("parametros.json", encoding="utf-8") # Abrimos archivo
PARAMETROS = json.load(archivo_parametros) # cargamos

class VentanaInterfaz(QWidget):

    # Senales
    senal_automatico = pyqtSignal()
    senal_manual = pyqtSignal()
    senal_mensaje = pyqtSignal(str)


    def __init__(self) -> None:

        super().__init__()
        ## Definimos geometria y nombre ventana
        self.setGeometry(80, 80, 1000, 1000)
        self.setWindowTitle("Interfaz")

        ## Definimos la estructura de la ventana
        self.init_gui()
    
    def init_gui(self):

        ## Fuentes

        self.fuente_info_1 = QFont('Arial', 30)
        self.fuente_info_1.setBold(True)

        self.fuente_info_2 = QFont('Arial', 16)
        self.fuente_info_2.setBold(True)


        ### Inicio Icono ###
        self.ruta_icono = join(*PARAMETROS["RUTA_ICONO"])
        self.setWindowIcon(QIcon(self.ruta_icono))
        ### --Fin Icono-- ###


        ### Inicio Selector Modo ###
        self.selector_modo = QComboBox()
        self.selector_modo.addItems(["Modo Calibración", "Modo Gráficos"])
        self.setWindowIcon(QIcon(self.ruta_icono))
        ### --Fin Selector Modo-- ###


        ### Inicio Botones ###
        self.boton_modo = QPushButton("Enviar", self)
        self.boton_modo.setFixedSize(50, 25)
        ### --Fin  Inicio Botones-- ###


        ### Inicio Espacio Video ###
        self.frame_video = CuadroVideo()
        
        ### -- Fin Espacio Video -- ###

        ### Inicio Info ###
        self.info_1 = QLabel("Modo Actual:")
        self.info_1.setAlignment(Qt.AlignCenter)
        self.info_1.setFont(self.fuente_info_2)
        self.info_1.setStyleSheet("color: black;")

        self.info_2 = QLabel("Modo Actual:")
        self.info_2.setAlignment(Qt.AlignCenter)
        self.info_2.setFont(self.fuente_info_2)
        self.info_2.setStyleSheet("color: black;")


        ### --Fin Info-- ###

        ### Inicio cambio de modo ###
        layout_modo = QHBoxLayout()
        layout_modo.addWidget(self.selector_modo)
        layout_modo.addWidget(self.boton_modo)
        ### --Fin Layout inferior-- ###


        ### Inicio Layout Superior Derecha ###
        layout_sup_der = QVBoxLayout()
        layout_sup_der.addWidget(self.info_1)
        layout_sup_der.addLayout(layout_modo)
        ### --Fin Layout Superior Derecha-- ###


        ### Inicio Layout Superior ###
        layout_superior = QHBoxLayout()
        layout_superior.addWidget(self.frame_video)
        layout_superior.addLayout(layout_sup_der)
        ### --Fin Layout Superior-- ###

        
        ### Inicio Layout Inf-Der ###
        layout_inf_der= QVBoxLayout()
        layout_inf_der.addWidget(self.info_2)
        ### --Fin Layout Sup-Der-- ###

        ### Inicio Layout Inferior ###
        layout_inferior = QHBoxLayout()
        layout_inferior.addStretch()
        layout_inferior.addLayout(layout_inf_der)
        ### --Fin Layout Inferior-- ###


        ### Inicio Layout principal ###
        layout = QVBoxLayout()
        layout.addLayout(layout_superior)
        layout.addLayout(layout_inferior)
        self.setLayout(layout)
        self.setFixedSize(1000, 1000)
        ### --Fin Layout principal-- ###

        ## Conectamos botones ##

        self.boton_modo.clicked.connect(self.enviar_modo)

    def cambiar_layout(self):
        if self.modo == "Calibración":
            pass
        else:
            pass

    ## Conexiones esperadas del back al front ##
    def cambiar_texto_info(self, texto: str) -> None:
        print(texto)
        self.info_1.setText(texto)
        self.info_1.show()
    
    def cambiar_frame_video(self, frame_recibido) -> None:
        self.frame_video.cambiar_frame(frame_recibido)
    
    ## Conexiones esperadas desde front al back ##
    
    def enviar_modo(self):
        texto_actual = str(self.selector_modo.currentText())
        print(texto_actual)
        
        if texto_actual == "Modo Calibración":
            self.senal_manual.emit()
        
        elif texto_actual == "Modo Gráficos":
            self.senal_automatico.emit()


    ## miscelaneo ##
    def abrir(self):
        self.show()

        