#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

#define SERVOMIN  150
#define SERVOMAX  600

const int BASE_CHANNEL     = 0;
const int SHOULDER_CHANNEL = 1;
const int ELBOW_CHANNEL    = 2;
const int GRIPPER_CHANNEL  = 3;

void setup() {
  Serial.begin(9600);
  pwm.begin();
  pwm.setPWMFreq(60);
  delay(10);
}

int angleToPulse(int angle) {
  return map(angle, 0, 180, SERVOMIN, SERVOMAX);
}

void loop() {
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    
    int c1 = data.indexOf(',');
    int c2 = data.indexOf(',', c1 + 1);
    int c3 = data.indexOf(',', c2 + 1);
    
    if (c1 > 0 && c2 > c1 && c3 > c2) {
      int baseAngle     = data.substring(0, c1).toInt();
      int shoulderAngle = data.substring(c1 + 1, c2).toInt();
      int elbowAngle    = data.substring(c2 + 1, c3).toInt();
      int gripperAngle  = data.substring(c3 + 1).toInt();
      
      pwm.setPWM(BASE_CHANNEL, 0, angleToPulse(baseAngle));
      pwm.setPWM(SHOULDER_CHANNEL, 0, angleToPulse(shoulderAngle));
      pwm.setPWM(ELBOW_CHANNEL, 0, angleToPulse(elbowAngle));
      pwm.setPWM(GRIPPER_CHANNEL, 0, angleToPulse(gripperAngle));
    }
  }
}