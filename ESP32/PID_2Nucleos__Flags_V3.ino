#include "esp_task.h"
#include <AccelStepper.h>
//#include <FreeRTOS.h>

// ... tus definiciones y variables globales ...

#define dirPinMotor1 12
#define stepPinMotor1 14
#define dirPinMotor2 2
#define stepPinMotor2 4
#define laser 25

#define motorInterfaceType 1 


AccelStepper stepper1(motorInterfaceType, stepPinMotor1, dirPinMotor1);
AccelStepper stepper2(motorInterfaceType, stepPinMotor2, dirPinMotor2);

volatile int x = 0;
volatile int y = 0;
volatile int x2 = 0;
volatile int y2 = 0;

float error_anteriorX = 0.0, error_anteriorY = 0.0;
float suma_erroresX1 = 0.0, suma_erroresY1 = 0.0, suma_erroresX2 = 0.0, suma_erroresY2 = 0.0;
const float kx1=0.1, kx2=0, ky1=0, ky2=0.1, kix1=0.00025, kix2=0, kiy1=0, kiy2=0.00025;

const int N = 20; 
float erroresX1[N];
float erroresY1[N];
float erroresX2[N];
float erroresY2[N];
int indiceX1 = 0;
int indiceY1 = 0;
int indiceX2 = 0;
int indiceY2 = 0;

String incomingData = "";

float PID_X(float setPointX, float currentX, float setPointY, float currentY) {
  
    // Implementación del PID para el eje X

    float delta_X=setPointX-currentX;
    float delta_Y=setPointY-currentY;
 
    suma_erroresX1 = suma_erroresX1 + delta_X - erroresX1[indiceX1];
    erroresX1[indiceX1] = delta_X;
    indiceX1 = (indiceX1 + 1) % N;


    
    
    suma_erroresY1 = suma_erroresY1 + delta_Y - erroresY1[indiceY1];
    erroresY1[indiceY1] = delta_Y;
    indiceY1 = (indiceY1 + 1) % N;
    float outputX=delta_X*kx1+delta_Y*ky1+suma_erroresX1*kix1+suma_erroresY1*kiy1;
    
    return outputX;
}

float PID_Y(float setPointX, float currentX, float setPointY, float currentY) {
    // Implementación del PID para el eje Y

    float delta_X=setPointX-currentX;
    float delta_Y=setPointY-currentY;
    

    suma_erroresX2 = suma_erroresX2 + delta_X - erroresX2[indiceX2];
    erroresX2[indiceX2] = delta_X;
    indiceX2 = (indiceX2 + 1) % N;
    
    suma_erroresY2 = suma_erroresY2 + delta_Y - erroresY2[indiceY2];
    erroresY2[indiceY2] = delta_Y;
    indiceY2 = (indiceY2 + 1) % N;
    float outputY=delta_X*kx2+delta_Y*ky2+suma_erroresX2*kix2+suma_erroresY2*kiy2;
    return outputY;
}

//////////////////////////////////////////////////
TaskHandle_t TaskSerialHandle;
TaskHandle_t TaskStepper1Handle;
TaskHandle_t TaskStepper2Handle;

void setup() {
  // Configura la comunicación serial, steppers y crea el semáforo
  Serial.begin(9600);

  stepper1.setMaxSpeed(3000*32); 
  stepper1.setAcceleration(1000*32); 
  
  stepper2.setMaxSpeed(3000*32);
  stepper2.setAcceleration(1000*32);

  // Crea las tareas en diferentes núcleos
  xTaskCreatePinnedToCore(TaskSerial, "TaskSerial", 10000, NULL, 1, &TaskSerialHandle, 0); // Tarea en el núcleo 0
  xTaskCreatePinnedToCore(TaskStepper1, "TaskStepper1", 10000, NULL, 1, &TaskStepper1Handle, 0); // También en núcleo 0
  xTaskCreatePinnedToCore(TaskStepper2, "TaskStepper2", 10000, NULL, 1, &TaskStepper2Handle, 1); // Tarea en núcleo 1
}

// Tarea para leer y procesar datos seriales
void TaskSerial(void *pvParameters) {
  String incomingData;
  for (;;) {
    if (Serial.available()!= 0) {
      incomingData = Serial.readStringUntil('\n');

      int idx1 = incomingData.indexOf(',');   // encuentra la primera coma
      int idx2 = incomingData.indexOf(',', idx1 + 1);  // encuentra la segunda coma
      int idx3 = incomingData.indexOf(',', idx2 + 1);  // encuentra la tercera coma

    if (idx1 != -1 && idx2 != -1 && idx3 != -1) {  // si encontramos todas las comas
      String xValue = incomingData.substring(0, idx1);  // extrae el valor x
      String yValue = incomingData.substring(idx1 + 1, idx2);  // extrae el valor y
      String x2Value = incomingData.substring(idx2 + 1, idx3);  // extrae el valor x2
      String y2Value = incomingData.substring(idx3 + 1);  // extrae el valor y2
      
      x = xValue.toInt();  
      y = yValue.toInt();  
      x2 = x2Value.toInt();  
      y2 = y2Value.toInt();  
      // Notifica a las tareas del motor que los nuevos datos están listos
      xTaskNotifyGive(TaskStepper1Handle);
      xTaskNotifyGive(TaskStepper2Handle);
    }
    vTaskDelay(1 / portTICK_PERIOD_MS); 
  }
}
}

// Tarea para controlar el stepper 1
void TaskStepper1(void *pvParameters) {
  for (;;) {
    // Espera una notificación para proceder
    ulTaskNotifyTake(pdTRUE, portMAX_DELAY);
    float outputX = PID_X( x2, x, y2, y);
    stepper1.move(outputX);
    stepper1.run();
  }
}

// Tarea para controlar el stepper 2
void TaskStepper2(void *pvParameters) {
  for (;;) {
    // Espera una notificación para proceder
    ulTaskNotifyTake(pdTRUE, portMAX_DELAY);
    float outputY = PID_Y(x2, x, y2, y);
    stepper2.move(outputY);
    stepper2.run();
  }
}



void loop() {
  // No es necesario hacer nada aquí
}
