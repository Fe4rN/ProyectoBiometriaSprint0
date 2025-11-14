// -*- mode: c++ -*-

#ifndef MEDIDOR_H_INCLUIDO
#define MEDIDOR_H_INCLUIDO

#include <Adafruit_TinyUSB.h>

// Pin 28, ANALOG4
#define sensorPin A4
#define vrefPin A5

// ------------------------------------------------------
// ------------------------------------------------------
class Medidor {

  // .....................................................
  // .....................................................
private:

public:

  // .....................................................
  // constructor
  // .....................................................
  Medidor() {
    pinMode(sensorPin, INPUT);
    pinMode(vrefPin, INPUT);
    Serial.begin(9600);
  }  // ()

  // .....................................................
  // .....................................................
  void iniciarMedidor() {
    // las cosas que no se puedan hacer en el constructor, if any
  }  // ()

  // .....................................................
  // .....................................................
  float medirCO2() {
    // Leer el valor analógico en el pin 28
    float lectura = analogRead(sensorPin);
    lectura = (lectura * 3.3) / 4096;
    float vref = analogRead(vrefPin);
    vref = (vref * 3.3) / 4096;

    float O3 = (lectura - vref);

    return 250000;
  }  // ()

  // .....................................................
  // .....................................................
  int medirTemperatura() {
    return -12;  // qué frío !
  }              // ()

};  // class

// ------------------------------------------------------
// ------------------------------------------------------
// ------------------------------------------------------
// ------------------------------------------------------
#endif
