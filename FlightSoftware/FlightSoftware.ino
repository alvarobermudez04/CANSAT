#include <Wire.h>
#include <SPI.h>
#include <Adafruit_Sensor.h>
#include "Adafruit_BMP3XX.h"

#define BMP_SCK 13
#define BMP_MISO 12
#define BMP_MOSI 11
#define BMP_CS 10

#define SEALEVELPRESSURE_HPA (1013.25)

Adafruit_BMP3XX bmp;

// Estados del cohete
enum RocketState {
  STANDBY,
  ASCENDING,
  FIRST_DESCEND,
  SECOND_DESCEND,
  THIRD_DESCEND,
  LANDED
};

// Variables
RocketState currentState = STANDBY;
float previousAltitude = 0.0;

void setup() {
  Serial.begin(9600);
  while (!Serial);
  Serial.println("Rocket Flight Computer Initialized");

  if (!bmp.begin_I2C()) {
    Serial.println("Could not find a valid BMP3 sensor, check wiring!");
    while (1);
  }

  bmp.setTemperatureOversampling(BMP3_OVERSAMPLING_8X);
  bmp.setPressureOversampling(BMP3_OVERSAMPLING_4X);
  bmp.setIIRFilterCoeff(BMP3_IIR_FILTER_COEFF_3);
  bmp.setOutputDataRate(BMP3_ODR_50_HZ);
}

void loop() {
  if (!bmp.performReading()) {
    Serial.println("Failed to perform reading :(");
    return;
  }
  
  float currentAltitude = bmp.readAltitude(SEALEVELPRESSURE_HPA);

  // Manejo de estados
  switch (currentState) {
    case STANDBY:
      if (currentAltitude > 0) {
        currentState = ASCENDING;
        Serial.println("Rocket has launched! Ascending...");
      }
      break;
      
    case ASCENDING:
      if (currentAltitude > previousAltitude) {
        // Continuar ascendiendo
        Serial.println("Ascending...");
      } else {
        currentState = FIRST_DESCEND;
        Serial.println("Apogee reached! Initiating first descend...");
      }
      break;
      
    case FIRST_DESCEND:
      if (currentAltitude < previousAltitude && currentAltitude > 100) {
        // Descender y activar heatshield
        Serial.println("First descend... Activating heatshield...");
      } else {
        currentState = SECOND_DESCEND;
        Serial.println("Heatshield activated! Initiating second descend...");
      }
      break;
      
    case SECOND_DESCEND:
      if (currentAltitude < previousAltitude && currentAltitude <= 100) {
        // Descender y activar parachute
        Serial.println("Second descend... Activating parachute...");
      } else {
        currentState = THIRD_DESCEND;
        Serial.println("Parachute activated! Initiating third descend...");
      }
      break;
      
    case THIRD_DESCEND:
      if (currentAltitude < previousAltitude) {
        // Continuar descendiendo
        Serial.println("Third descend...");
      } else {
        currentState = LANDED;
        Serial.println("Rocket has landed! Activating beacon...");
      }
      break;
      
    case LANDED:
      if (currentAltitude == 0) {
        Serial.println("Beacon activated. Mission complete!");
      }
      break;
  }

  // Actualizar la altitud anterior
  previousAltitude = currentAltitude;

  delay(1000); // Realizar lectura cada segundo
}
