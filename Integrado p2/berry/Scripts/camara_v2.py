import cv2 as cv
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import serial
from PyQt5.QtCore import pyqtSignal, QThread



class Camara(QThread):

    senal_video = pyqtSignal(list)
    senal_filtrado = pyqtSignal(list)

    def __init__(self, parent):
        super().__init__(parent)
        self.lower_bound = np.array([0, 0, 0])
        self.upper_bound = np.array([255, 255, 255])
        self.calibrated = False
        self.camera = PiCamera()
        self.frame = None
        self.filtered_frame = None
        self.ser = serial.Serial('/dev/ttyUSB0', 9600)  
    
    def run(self):
        self.camera.resolution = (640, 480)
        self.camera.framerate = 32
        time.sleep(0.1)
        rawCapture = PiRGBArray(self.camera, size=(640, 480))
        cv.namedWindow('Original Image')
        cv.setMouseCallback('Original Image', self.calibrate_color)

        for capture in self.camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            self.frame = capture.array

            # Filtrar los colores dentro del rango seleccionado
            mask = cv.inRange(self.frame, self.lower_bound, self.upper_bound)
            self.filtered_frame = cv.bitwise_and(self.frame, self.frame, mask=mask)

            if self.calibrated:
                # Encontrar el contorno del punto láser
                contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

                for contour in contours:
                    # Calcular el centroide del contorno
                    M = cv.moments(contour)
                    if M["m00"] != 0:
                        cX = int(M["m10"] / M["m00"])
                        cY = int(M["m01"] / M["m00"])

                        if int(cX) > 320 and int(cY) >240:
                            self.ser.write(b'U')
                        elif int(cX) < 320 and int(cY) >240:
                            self.ser.write(b'D')
                        elif int(cX) < 320 and int(cY) <240:
                            self.ser.write(b'R')
                        elif int(cX) > 320 and int(cY) <240:
                            self.ser.write(b'L') 

                        # Dibujar el centroide en el frame original y el filtrado
                        cv.circle(self.frame, (cX, cY), 5, (255, 0, 0), -1)
                        cv.circle(self.filtered_frame, (cX, cY), 5, (255, 0, 0), -1)

                        # Dibujar la posición en la parte superior izquierda del frame
                        position_str = f"X: {cX}, Y: {cY}"
                        cv.putText(self.frame, position_str, (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
                        cv.putText(self.filtered_frame, position_str, (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

            # Mostrar las imágenes
            cv.imshow('Original Image', self.frame)
            cv.imshow('Filtered Colors', self.filtered_frame)

            # Enviar senal de video
            self.senal_video.emit([self.frame])

            # Limpia el stream para la siguiente captura
            rawCapture.truncate(0)

            # Salir del bucle si se presiona la tecla 'q'
            if cv.waitKey(1) & 0xFF == ord('q'):
                break

            cv.destroyAllWindows()
    
    def calibrate_color(self, event, x, y, flags, param):
        if event == cv.EVENT_LBUTTONDOWN:
            color = self.frame[y, x]
            self.lower_bound = np.array([color[0] - 40, color[1] - 40, color[2] - 100])
            self.upper_bound = np.array([color[0] + 40, color[1] + 40, color[2] + 100])
            self.calibrated = True
