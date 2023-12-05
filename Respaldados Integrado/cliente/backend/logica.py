from PyQt5.QtCore import QObject, pyqtSignal




class Logica(QObject):

    senal_modo_actual_recibido = pyqtSignal(str) # Manual o Autmatico
    
    senal_video = pyqtSignal(list)

    senal_mensaje = pyqtSignal(list) # mensaje de salida

    def __init__(self) -> None:
        super().__init__()
    
    
    def mandar_automatico(self):
        mensaje = ["modo","Automatico"]
        self.senal_mensaje.emit(mensaje)
    
    def mandar_manual(self):
        mensaje = ["modo","Manual"]
        self.senal_mensaje.emit(mensaje)
    
    def mandar_mensaje_escrito(self, mensaje :str):
        self.senal_mensaje.emit(["escrito", mensaje])
    

    #### Manejo mensajes ####

    def manejo_mensajes_tcp(self, mensaje: list):
        """
        Dependiendo del mensaje recibido se realizaran diversas
        acciones de emision de senales al llamarse a las funciones
        """
        #print("Llego desde lejos", mensaje)
        
        comando = mensaje[0]
        contenido = mensaje[1]

        if comando == "modo":
            self.senal_modo_actual_recibido.emit(contenido)


    def manejo_mensajes_udp(self, mensaje: list):
        pass
        

        


        



        

        

        

    




    
