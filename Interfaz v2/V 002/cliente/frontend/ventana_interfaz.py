import typing
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (QWidget, QLabel, QPushButton)
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QLineEdit
from PyQt5.QtGui import  QPixmap, QIcon, QFont, QImage
import json
from os.path import join

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
        self.setGeometry(100, 100, 775, 700)
        self.setWindowTitle("Interfaz")

        ## Definimos la estructura de la ventana
        self.init_gui()
    
    def init_gui(self):

        ## Fuentes

        self.fuente_info = QFont('Arial', 30)
        self.fuente_info.setBold(True)

        ### Inicio Icono ###
        self.ruta_icono = join(*PARAMETROS["RUTA_ICONO"])
        self.setWindowIcon(QIcon(self.ruta_icono))
        ### --Fin Icono-- ###

        ### Inicio Botones ###
        self.boton_manual = QPushButton("Modo Manual", self)
        self.boton_manual.setFixedSize(100, 50)
        self.boton_automatico = QPushButton("Modo Automático", self)
        self.boton_automatico.setFixedSize(100, 50)
        ### --Fin  Inicio Botones-- ###

        ### Inicio Linea Editable ###
        self.texto_prueba = QLabel("Mensaje:", self)
        self.linea_editable = QLineEdit(self)
        self.boton_envio = QPushButton("Enviar", self)
        self.boton_envio.setFixedSize(80, 50)
        ### Fin Linea Editable ###

        ### Inicio Espacio Video ###
        self.label_video = QLabel(self)
        self.label_video.setFixedSize(320, 240)
        ### -- Fin Espacio Video -- ###

        ### Inicio Info ###
        self.info_1 = QLabel("Info de prueba")
        self.info_1.setAlignment(Qt.AlignCenter)
        self.info_1.setFont(self.fuente_info)
        self.info_1.setStyleSheet("color: black;")
        ### --Fin Info-- ###

        ### Inicio Layout inferior ###
        layout_inferior = QHBoxLayout()
        layout_inferior.addWidget(self.boton_manual)
        layout_inferior.addWidget(self.boton_automatico)
        ### --Fin Layout inferior-- ###


        ### Inicio Layout Sup-Der ###
        layout_derecha = QHBoxLayout()
        layout_derecha.addWidget(self.texto_prueba)
        layout_derecha.addWidget(self.linea_editable)
        layout_derecha.addWidget(self.boton_envio)
        ### --Fin Layout Sup-Der-- ###

        
        ### Inicio Layout Sup-Izq ###
        layout_izquierda= QHBoxLayout()
        layout_izquierda.addWidget(self.info_1)
        ### --Fin Layout Sup-Der-- ###

        ### Inicio Layout Superior ###
        layout_superior = QHBoxLayout()
        layout_superior.addLayout(layout_izquierda)
        layout_superior.addStretch()
        layout_superior.addLayout(layout_derecha)
        ### --Fin Layout Superior-- ###

        ### Inicio Layout principal ###
        layout = QVBoxLayout()
        layout.addLayout(layout_superior)
        layout.addLayout(layout_inferior)
        self.setLayout(layout)
        self.setFixedSize(775, 700)
        ### --Fin Layout principal-- ###

        ## Conectamos botones ##

        self.boton_manual.clicked.connect(self.manual)
        self.boton_automatico.clicked.connect(self.automatico)
        self.boton_envio.clicked.connect(self.envio)


    ## Conexiones esperadas del back al front ##
    def cambiar_texto_info(self, texto: str) -> None:
        self.info_1.setText(texto)
        self.info_1.show()
    
    def cambiar_frame_video(self, frame) -> None:
        self.label_video.setPixmap(QPixmap.fromImage(frame))
    
    ## Conexiones esperadas desde front al back ##
    def manual(self) -> None:
        self.senal_manual.emit()

    def automatico(self) -> None:
        self.senal_automatico.emit()

    def envio(self) -> None:
        mensaje = self.linea_editable.text()
        print(mensaje)
        self.senal_mensaje.emit(mensaje)
        
    ## miscelaneo ##
    def abrir(self):
        self.show()

        