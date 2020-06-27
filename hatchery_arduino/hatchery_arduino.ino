#include <OneWire.h>
#include <DallasTemperature.h>
#include "ph_grav.h"                           
// PH setup
Gravity_pH pH = Gravity_pH(A1);

// Temperature setup
// Data wire is plugged into digital pin 2 on the Arduino
#define ONE_WIRE_BUS 2

// Setup a oneWire instance to communicate with any OneWire device
OneWire oneWire(ONE_WIRE_BUS);  

// Pass oneWire reference to DallasTemperature library
DallasTemperature sensors(&oneWire);

int deviceCount = 0;
float tempC;


void setup() {
  sensors.begin();  // Start up the library 
  deviceCount = sensors.getDeviceCount();
//  pinMode(13,OUTPUT); for writing to a pin, not currently doing
  Serial.begin(9600);
}

void loop() {
  // Wait a second between measurements.
  delay(1000);
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
