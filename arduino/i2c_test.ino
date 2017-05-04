#include <Wire.h>
const byte slaveAddr = 0x50;
int registerAddr;


void loop() {
  // put your main code here, to run repeatedly:
  delay(1000);
}

void receiveRegister(int x){
  registerAddr = Wire.read();
}

void respondData(){
  Wire.write(registerAddr);
}

void setup() {
  TWBR=100000L;
  Wire.begin(slaveAddr);
  Wire.onReceive(receiveRegister);
  Wire.onRequest(respondData);
} 
