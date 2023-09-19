import cv2 as cv
from matplotlib import pyplot as plt

# Inicializar la cámara
cap = cv.VideoCapture(0)

while True:
    # Capturar un solo frame
    ret, frame = cap.read()
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    
    # Aplicar filtro
    gray_frame = cv.medianBlur(gray_frame, 5)
    
    # Aplicar diferentes tipos de umbralización
    ret, th1 = cv.threshold(gray_frame, 127, 255, cv.THRESH_BINARY)
    th2 = cv.adaptiveThreshold(gray_frame, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 11, 2)
    th3 = cv.adaptiveThreshold(gray_frame, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11, 2)
    

    # Mostrar las imágenes
    #cv.imshow('Original Image', gray_frame)
    cv.imshow('Global Thresholding (v = 127)', th1)
    cv.imshow('Adaptive Mean Thresholding', th2)
    cv.imshow('Adaptive Gaussian Thresholding', th3)
    
    # Salir del bucle si se presiona la tecla 'q'
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar la cámara y destruir todas las ventanas de OpenCV
cap.release()
cv.destroyAllWindows()
