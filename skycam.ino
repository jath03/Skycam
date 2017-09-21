#include <Wire.h>
#include <Servo.h>

const byte slaveAddr = 0x50;
int registerAddr;
String value = "";
String toSend = "";
int i = 0;
int drive1Pin = 5;
int drive2Pin = 6;
int panPin = 10;
int tiltPin = 11;
Servo drive1;
Servo drive2;
Servo pan;
Servo tilt;



void off() {
  digitalWrite(7, HIGH);
  delay(20000);
  digitalWrite(8, HIGH);
  digitalWrite(7, LOW);
}

String getDriveDirection() {
  int g = drive1.read();
  if (g > 90) {
    return "1";
  } else if (g < 90) {
    return "0";
  } else {
    return "2";
  }
}

void center() {
  pan.write(180);
  tilt.write(90);
}

void parseString(String s) {
  int comma = s.indexOf(',');
  String command = s.substring(0, comma);
  int value = s.substring(comma + 1).toInt();
  if (command == "move") {
    if (value == 0) {
      drive1.write(45);
      drive2.write(45);
      toSend = getDriveDirection();
    }
    else if (value == 1) {
      drive1.write(135);
      drive2.write(135);
      toSend = getDriveDirection();
    }
    else if (value == -1) {
      toSend = getDriveDirection();
    }
    else {
      drive1.write(90);
      drive2.write(90);
      toSend = getDriveDirection();
    }
  }
  else if (command == "pan") {
    if (value == 0) {
      int cv = pan.read();
      pan.write(cv + 5);
      toSend = String(cv + 5);
    } else if (value == 1) {
      int cv = pan.read();
      pan.write(cv - 5);
      toSend = String(cv - 5);
    } else if (value == -1) {
      toSend = String(pan.read());
    } else {
      pan.write(180);
    }
  }
  else if (command == "tilt") {
    if (value == 0) {
      int cv = tilt.read();
      tilt.write(cv + 5);
      toSend = String(cv + 5);
    } else if (value == 1) {
      int cv = tilt.read();
      tilt.write(cv - 5);
      toSend = String(cv - 5);
    } else if (value == -1) {
      toSend = String(tilt.read());
    } else {
      tilt.write(135);
    }
  }
}

void receiveRegister(int x){
  int inChar;
  inChar = Wire.read();
  if(char(inChar) != '\n'){
    value += char(inChar);
  }
  else {
    Serial.print("I Recieved ");
    Serial.println(value);
    parseString(value);
    value = "";
  }
}

void respondData(){
  int len = toSend.length()+1;
  if(i+1<len){
    char ascii_num[len];
    toSend.toCharArray(ascii_num, len);
    Serial.print("Sending char ");
    Serial.println(ascii_num[i]);
    Wire.write(ascii_num[i]);
    i += 1;
  }
  else {
    Wire.write('\n');
    i = 0;
  }
}

void loop() {
  // put your main code here, to run repeatedly:
  delay(100);
  if (digitalRead(12)) {
    off();
  }
}

void setup() {
  TWBR=100000L;
  Serial.begin(9600);
  Wire.begin(slaveAddr);
  Wire.onReceive(receiveRegister);
  Wire.onRequest(respondData);
  drive1.attach(drive1Pin);
  drive2.attach(drive2Pin);
  pan.attach(panPin);
  tilt.attach(tiltPin);
  drive1.write(90);
  drive2.write(90);
  pan.write(180);
  tilt.write(135);
  pinMode(7, OUTPUT);
  digitalWrite(7, LOW);
  pinMode(8, OUTPUT);
  digitalWrite(7, LOW);
  pinMode(12, INPUT);
  delay(500);
}
