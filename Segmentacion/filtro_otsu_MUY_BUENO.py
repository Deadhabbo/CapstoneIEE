import cv2 as cv

# Inicializar la cámara
cap = cv.VideoCapture(0)
width, height = 1000, 500  # Dimensiones deseadas

while True:
    # Capturar un solo frame
    ret, frame = cap.read()
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    
    # Reducir resolución
    gray_frame = cv.resize(gray_frame, (width, height))
    
    # Aplicar filtro Gaussiano
    blur = cv.GaussianBlur(gray_frame, (5, 5), 0)
    
    # Otsu's thresholding
    ret3, th3 = cv.threshold(blur, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    
    # Mostrar solo la imagen con umbralización de Otsu
    cv.imshow('Otsu Thresholding', th3)
    
    # Salir del bucle si se presiona la tecla 'q'
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar la cámara y destruir todas las ventanas de OpenCV
cap.release()
cv.destroyAllWindows()

