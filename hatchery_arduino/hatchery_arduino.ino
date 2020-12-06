#include <OneWire.h>
#include <DallasTemperature.h>
#include "ph_grav.h"
// PH setup
Gravity_pH pH = Gravity_pH(A2);

// Temperature setup
// Data wire is plugged into digital pin 2 on the Arduino
#define ONE_WIRE_BUS 2

// pump setup
int motorPin1 = A0; // pin that turns on the motor
int motorPin2 = A4; // pin that turns on the motor

// Setup a oneWire instance to communicate with any OneWire device
OneWire oneWire(ONE_WIRE_BUS);

// Pass oneWire reference to DallasTemperature library
DallasTemperature sensors(&oneWire);

int deviceCount = 0;
float tempC;


void setup() {
  sensors.begin();  // Start up the library
  deviceCount = sensors.getDeviceCount();
  pinMode(motorPin1, OUTPUT); // set A0 to an output so we can use it to turn on the transistor
  pinMode(motorPin2, OUTPUT); // set A0 to an output so we can use it to turn on the transistor
  Serial.begin(9600);
}

void loop() {
  // Wait a second between measurements.
  delay(1000);
  // check for pump change
  if (Serial.available()) {
        char serialListener = Serial.read();
        if (serialListener == 'H') {
            digitalWrite(motorPin1, HIGH);
        }
        else if (serialListener == 'I') {
            digitalWrite(motorPin2, HIGH);
        }
        else if (serialListener == 'J') {
            digitalWrite(motorPin1, HIGH);
            digitalWrite(motorPin2, HIGH);
        }
        else if (serialListener == 'K') {
            digitalWrite(motorPin1, LOW);
        }
        else if (serialListener == 'L') {
            digitalWrite(motorPin2, LOW);
        }
        else if (serialListener == 'M') {
            digitalWrite(motorPin1, LOW);
            digitalWrite(motorPin2, LOW);
        }
    }
  //Temp acquisition
  sensors.requestTemperatures();

  for (int i = 0;  i < deviceCount;  i++)
  {
    tempC = sensors.getTempCByIndex(i);
    Serial.print(" ");
    Serial.print(DallasTemperature::toFahrenheit(tempC));
  }
  Serial.print(" ");
  Serial.println(pH.read_ph());
//  digitalWrite(13, HIGH); for writing to a pin, not currently doing
//  delay(800);
//  digitalWrite(13, LOW); for writing to a pin, not currently doing
}
