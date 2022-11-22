#include <AFMotor.h>

AF_DCMotor motor1(3);
AF_DCMotor motor2(4);

void setup() {
  motor1.setSpeed(200);
  motor2.setSpeed(200);
  motor1.run(RELEASE);
  motor2.run(RELEASE);
}

void loop() {  

  //초음파센서 장애물 감지;

  motor1.run(FORWARD); //전진
  motor2.run(FORWARD);
  delay(1000);
}
