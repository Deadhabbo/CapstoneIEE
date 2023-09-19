import cv2 as cv
import numpy as np

# Función de calibración de color
def calibrate_color(event, x, y, flags, param):
    global lower_bound, upper_bound, calibrated

    if event == cv.EVENT_LBUTTONDOWN:
        color = frame[y, x]
        lower_bound = np.array([color[0] - 60, color[1] - 60, color[2] - 120])
        upper_bound = np.array([color[0] + 60, color[1] + 60, color[2] + 120])
        calibrated = True

# Inicializar la cámara
cap = cv.VideoCapture(0)

# Valores iniciales para los límites inferior y superior
lower_bound = np.array([0, 0, 0])
upper_bound = np.array([255, 255, 255])
calibrated = False  # Indicador de calibración

cv.namedWindow('Original Image')
cv.setMouseCallback('Original Image', calibrate_color)

while True:
    # Capturar un solo frame
    ret, frame = cap.read()

    # Filtrar los colores dentro del rango seleccionado
    mask = cv.inRange(frame, lower_bound, upper_bound)
    filtered_frame = cv.bitwise_and(frame, frame, mask=mask)

    if calibrated:
        # Encontrar el contorno del punto láser
        contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            # Calcular el centroide del contorno
            M = cv.moments(contour)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])

                # Dibujar el centroide en el frame original y el filtrado
                cv.circle(frame, (cX, cY), 5, (255, 0, 0), -1)
                cv.circle(filtered_frame, (cX, cY), 5, (255, 0, 0), -1)

                # Dibujar la posición en la parte superior izquierda del frame
                position_str = f"X: {cX}, Y: {cY}"
                cv.putText(frame, position_str, (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
                cv.putText(filtered_frame, position_str, (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    # Mostrar las imágenes
    cv.imshow('Original Image', frame)
    cv.imshow('Filtered Colors', filtered_frame)

    # Salir del bucle si se presiona la tecla 'q'
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar la cámara y destruir todas las ventanas de OpenCV
cap.release()
cv.destroyAllWindows()
