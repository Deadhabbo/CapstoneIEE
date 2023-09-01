from PyQt5.QtCore import QObject, pyqtSignal




class Logica(QObject):
    senal_nombre = pyqtSignal(int, str) # indice nombre
    senal_espera = pyqtSignal(str) # mensaje espera
    senal_inicio_partida = pyqtSignal() 
    senal_retornar = pyqtSignal()

    senal_cambio_dado = pyqtSignal(int, int, int) 
    senal_nombre_jugador = pyqtSignal(str, int)
    senal_vida_jugador = pyqtSignal(str, int)
    senal_tiempo = pyqtSignal(str)
    senal_poder = pyqtSignal(bool)
    senal_cuenta = pyqtSignal(str)
    senal_nombre_actual = pyqtSignal(str)
    senal_nombre_pasado = pyqtSignal(str)
    senal_turno = pyqtSignal(str)

    senal_mensaje = pyqtSignal(list) # mensaje de salida

    def __init__(self) -> None:
        super().__init__()
    
    
    def mandar_automatico(self):
        mensaje = ["Automatico"]
        self.senal_mensaje.emit(mensaje)
    
    def mandar_manual(self):
        mensaje = ["Manual"]
        self.senal_mensaje.emit(mensaje)
    
    def mandar_mensaje_escrito(self, mensaje :str):
        self.senal_mensaje.emit([mensaje])
    

    #### Manejo mensajes ####

    def manejo_mensajes(self, mensaje: list):
        """
        Dependiendo del mensaje recibido se realizaran diversas
        acciones de emision de senales al llamarse a las funciones
        """
        #print("Llego desde lejos", mensaje)
        pass

        

        


        



        

        

        

    




    
