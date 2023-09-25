#include <AccelStepper.h>


#define dirPinMotor1 12
#define stepPinMotor1 14
#define dirPinMotor2 2
#define stepPinMotor2 4

#define motorInterfaceType 1 


AccelStepper stepper1(motorInterfaceType, stepPinMotor1, dirPinMotor1);
AccelStepper stepper2(motorInterfaceType, stepPinMotor2, dirPinMotor2);

void setup() {
  Serial.begin(115200);
  stepper1.setMaxSpeed(300); 
  stepper1.setAcceleration(100); 
  
  stepper2.setMaxSpeed(300);
  stepper2.setAcceleration(100);
}

void loop() {
  if (Serial.available()) {
    String input = Serial.readStringUntil('\n');
    
    
    int commaIndex = input.indexOf(',');
    long x = input.substring(0, commaIndex).toInt();
    long y = input.substring(commaIndex + 1).toInt();
    
    moveToXY(x, y);
  }
}

void moveToXY(long x, long y) {
  if (x != 0) {
    
    stepper1.moveTo(x);
    stepper2.moveTo(x);
  } else if (y != 0) {
    
    stepper1.moveTo(y);
  }

 
  while (stepper1.distanceToGo() != 0 || stepper2.distanceToGo() != 0) {
    stepper1.run();
    stepper2.run();
  }
}
