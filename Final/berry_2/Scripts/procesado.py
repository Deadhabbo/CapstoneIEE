import cv2 as cv
import numpy as np
import time
import serial
import csv
from threading import Thread

class Procesado:

    def __init__(self, camara):
        # initialize the thread
        super().__init__()
        self.camara = camara
        self.lower_bound_red = np.array([0, 0, 0])
        self.upper_bound_red = np.array([255, 255, 255])
        self.lower_bound_blue = np.array([0, 0, 0])
        self.upper_bound_blue = np.array([255, 255, 255])

        #self.ser = serial.Serial('/dev/ttyUSB0', 9600)
    
    def calibrate_color(self, boton ,x, y):
        color = self.camara.frame[y,x]

        if boton == "Izquierdo":
            self.lower_bound_red = np.array([color[0] - 40, color[1] - 40, color[2] - 100])
            self.upper_bound_red = np.array([color[0] + 40, color[1] + 40, color[2] + 100])
        
        elif boton == "Derecho":
            hsv_color = cv.cvtColor(np.uint8([[color]]), cv.COLOR_BGR2HSV)[0][0]
            self.lower_bound_blue = np.array([hsv_color[0] - 10, 100, 100])
            self.upper_bound_blue = np.array([hsv_color[0] + 10, 255, 255])
        
    
    def procesar(self):
        frame = self.camara.frame
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        mask_red = cv.inRange(frame, self.lower_bound_red, self.upper_bound_red)
        mask_blue = cv.inRange(hsv, self.lower_bound_blue, self.upper_bound_blue)

        #filtered_frame_red = cv.bitwise_and(frame, frame, mask=mask_red)
        #filtered_frame_blue = cv.bitwise_and(frame, frame, mask=mask_blue)

        # Procesamiento de contornos rojos
        contours_red, _ = cv.findContours(mask_red, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        if contours_red:
            largest_contour_red = max(contours_red, key=cv.contourArea)
            M = cv.moments(largest_contour_red)

            if M["m00"] != 0:
                cX1 = int(M["m10"] / M["m00"])
                cY1 = int(M["m01"] / M["m00"])
                cv.circle(frame, (cX1, cY1), 5, (0, 0, 255), -1)
                position_str = f"X1: {cX1}, Y1: {cY1}"
                cv.putText(frame, position_str, (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Procesamiento de contornos azules
        contours_blue, _ = cv.findContours(mask_blue, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        if contours_blue:
            largest_contour_blue = max(contours_blue, key=cv.contourArea)
            M = cv.moments(largest_contour_blue)

            if M["m00"] != 0:
                cX2 = int(M["m10"] / M["m00"])
                cY2 = int(M["m01"] / M["m00"])
                cv.circle(frame, (cX2, cY2), 5, (255, 0, 0), -1)

                # Dibujar la posición en la parte superior izquierda del frame
                position_str = f"X2: {cX2}, Y2: {cY2}"
                cv.putText(frame, position_str, (10, 80), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        data_string = "{},{},{},{}\n".format(cX1, cY1, cX2, cY2)
        #self.ser.write(data_string.encode())

        # Escribir las coordenadas en el archivo CSV
        #csv_writer.writerow([cX1, cY1, cX2, cY2])

        # cv.imshow('Original Image', frame)
        # cv.imshow('Filtered Red Colors', filtered_frame_red)
        # cv.imshow('Filtered Blue Colors', filtered_frame_blue)

        #rawCapture.truncate(0)

        # if cv.waitKey(1) & 0xFF == ord('q'):
        #     break



