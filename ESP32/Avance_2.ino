#include <AccelStepper.h>

#define dirPinMotor1 12
#define stepPinMotor1 14
#define dirPinMotor2 2
#define stepPinMotor2 4


#define motorInterfaceType 1 


AccelStepper stepper1(motorInterfaceType, stepPinMotor1, dirPinMotor1);
AccelStepper stepper2(motorInterfaceType, stepPinMotor2, dirPinMotor2);
char option = ' ';
void setup() {
  Serial.begin(9600);
  stepper1.setMaxSpeed(3000*32); 
  stepper1.setAcceleration(1000*32); 
  
 stepper2.setMaxSpeed(3000*32);
 stepper2.setAcceleration(1000*32);
}

void loop() {
  if (Serial.available() != 0) {
    option = Serial.read();
    
    if (option == 'R') {
      
      stepper1.move(800); 
       
    } else if (option == 'L') {
      stepper1.move(-800); 
      
       
    } else if (option == 'D'){
      stepper2.move(800);
      stepper1.move(800);
      
    } else if (option == 'U'){
      stepper2.move(-800);
      stepper1.move(-800);
    }
    
  }
  // Mueve los motores paso a paso hacia sus posiciones objetivo en cada iteración del bucle
  stepper1.run();
  stepper2.run();
}
