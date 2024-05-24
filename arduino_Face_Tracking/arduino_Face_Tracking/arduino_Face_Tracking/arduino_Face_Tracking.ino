#include <cvzone.h>
#include <Servo.h>

SerialData serialData(2,3);
Servo servoHor;
Servo servoVer;

int valsRec[2];

void setup() {
  serialData.begin();
  servoHor.attach(10);
  servoVer.attach(9);

}

void loop() {
  serialData.Get(valsRec);
  servoHor.write(valsRec[0]);
  servoVer.write(valsRec[1]);  
}
