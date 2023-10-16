#include "esp_task.h"
#include <AccelStepper.h>

#define dirPinMotor1 12
#define stepPinMotor1 14
#define dirPinMotor2 2
#define stepPinMotor2 4

#define motorInterfaceType 1 


AccelStepper stepper1(motorInterfaceType, stepPinMotor1, dirPinMotor1);
AccelStepper stepper2(motorInterfaceType, stepPinMotor2, dirPinMotor2);

float x1, y1, x2, y2;
float error_anteriorX = 0.0, error_anteriorY = 0.0;
float suma_erroresX1 = 0.0, suma_erroresY1 = 0.0, suma_erroresX2 = 0.0, suma_erroresY2 = 0.0;
const float kx1=10, kx2=0, ky1=0, ky2=10, kix1=5, kix2=1, kiy1=2, kiy2=5;

// Pseudocódigo para las funciones de PID
float PID_X(float setPointX, float currentX, float setPointY, float currentY) {
  
    // Implementación del PID para el eje X

    delta_X=setPointX-currentX;
    delta_Y=setPointY-currentY;
    suma_erroresX1+=delta_X;
    suma_erroresY1+=delta_Y;
    outputX=delta_X*kx1+delta_Y*ky1+suma_erroresX1*kix1+suma_erroresY1*kiy1;
    
    return outputX;
}

float PID_Y(float setPointY, float currentY, float setPointX, float currentX) {
    // Implementación del PID para el eje Y

    delta_X=setPointX-currentX;
    delta_Y=setPointY-currentY;
    suma_erroresX2+=delta_X;
    suma_erroresY2+=delta_Y;
    outputY=delta_X*kx2+delta_Y*ky2+suma_erroresX2*kix2+suma_erroresY2*kiy2;
    return outputY;
}

bool leerCoordenadas() {
    String data = "";
    if (Serial.available()) {
        // Leer x1
        while (Serial.peek() != ',' && Serial.available()) {
            data += (char)Serial.read();
            delay(10);  // Dar tiempo a la llegada de nuevos caracteres
        }
        Serial.read();  // Leer y descartar la coma
        x1 = data.toFloat();
        data = "";

        // Leer y1
        while (Serial.peek() != ',' && Serial.available()) {
            data += (char)Serial.read();
            delay(10);
        }
        Serial.read();
        y1 = data.toFloat();
        data = "";

        // Leer x2
        while (Serial.peek() != ',' && Serial.available()) {
            data += (char)Serial.read();
            delay(10);
        }
        Serial.read();
        x2 = data.toFloat();
        data = "";

        // Leer y2
        while (Serial.available()) {
            data += (char)Serial.read();
            delay(10);
        }
        y2 = data.toFloat();
        return true;  // Retornar verdadero si se leyeron todas las coordenadas
    }
    return false;  // Retornar falso si no había datos disponibles
}

// Tareas para los núcleos
void Task_Core0(void *pvParameters) {
    while(1) {
        if (leerCoordenadas()) {
            float outputX = PID_X(x2, x1, y2, y1);
            stepper1.move(outputX);  // Función ficticia para aplicar el resultado del PID a lo que estés controlando
        }
        delay(100);  // Puedes ajustar este delay según lo que necesites
    }
}

void Task_Core1(void *pvParameters) {
    while(1) {
        if (leerCoordenadas()) {
            float outputY = PID_Y(y1, y2, x2, x1);
            stepper2.move(outputY);  // Función ficticia para aplicar el resultado del PID a lo que estés controlando
        }
        delay(100);  // Puedes ajustar este delay según lo que necesites
    }
}

void setup() {
    Serial.begin(115200);  // Iniciar comunicación serial
    stepper1.setMaxSpeed(3000*32); 
    stepper1.setAcceleration(1000*32); 
  
    stepper2.setMaxSpeed(3000*32);
    stepper2.setAcceleration(1000*32);
    delay(1000);  // Dar tiempo para que la comunicación serial se establezca

    xTaskCreatePinnedToCore(
        Task_Core0,  /* Función de la tarea */
        "Task_Core0", /* Nombre de la tarea */
        10000,       /* Tamaño del stack de la tarea */
        NULL,        /* Parámetros de la tarea */
        1,           /* Prioridad de la tarea */
        NULL,        /* Handle de la tarea */
        0);          /* Núcleo donde se ejecutará la tarea */

    xTaskCreatePinnedToCore(
        Task_Core1,
        "Task_Core1",
        10000,
        NULL,
        1,
        NULL,
        1);  // Ejecutar en el núcleo 1
}

void loop() {
    // Código principal. No hay necesidad de poner nada aquí ya que estás usando tareas.
}
