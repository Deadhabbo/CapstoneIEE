import cv2 as cv
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import serial
import csv

# Inicializar conexión serial
ser = serial.Serial('/dev/ttyUSB0', 9600)
time.sleep(2)

# Función de calibración de color
def calibrate_color(event, x, y, flags, param):
    global lower_bound_red, upper_bound_red, lower_bound_green, upper_bound_green, color_to_calibrate

    if event == cv.EVENT_LBUTTONDOWN:
        color = frame[y, x]
        if color_to_calibrate == "red":
            lower_bound_red = np.array([color[0] - 40, color[1] - 40, color[2] - 100])
            upper_bound_red = np.array([color[0] + 40, color[1] + 40, color[2] + 100])
            color_to_calibrate = "green"
        elif color_to_calibrate == "green":
            # Ajuste de los límites para el color verde en el espacio RGB
            lower_bound_green = np.array([color[0] - 40, color[1] - 40, color[2] - 40])
            upper_bound_green = np.array([color[0] + 40, color[1] + 40, color[2] + 40])
            color_to_calibrate = "red"

# Inicializar la cámara
camera = PiCamera()
camera.resolution = (480, 360)
camera.framerate = 60
rawCapture = PiRGBArray(camera, size=(480, 360))
time.sleep(0.1)

# Valores iniciales
lower_bound_red = np.array([0, 0, 0])
upper_bound_red = np.array([255, 255, 255])
lower_bound_green = np.array([0, 0, 0])
upper_bound_green = np.array([255, 255, 255])
color_to_calibrate = "red"
a =[]

cv.namedWindow('Original Image')
cv.setMouseCallback('Original Image', calibrate_color)

# Abre un archivo CSV en modo de escritura

for capture in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    frame = capture.array
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    mask_red = cv.inRange(frame, lower_bound_red, upper_bound_red)
    mask_green = cv.inRange(frame, lower_bound_green, upper_bound_green)

    filtered_frame_red = cv.bitwise_and(frame, frame, mask=mask_red)
    filtered_frame_green = cv.bitwise_and(frame, frame, mask=mask_green)

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
    contours_blue, _ = cv.findContours(mask_green, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
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
    ser.write(data_string.encode())

    # Escribir las coordenadas en el archivo CSV
    #csv_writer.writerow([cX1, cY1, cX2, cY2])
    #a.append([cX1, cY1, cX2, cY2])
    cv.imshow('Original Image', frame)
    cv.imshow('Filtered Red Colors', filtered_frame_red)
    cv.imshow('Filtered Blue Colors', filtered_frame_green)

    rawCapture.truncate(0)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cv.destroyAllWindows()