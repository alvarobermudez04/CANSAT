#include <Wire.h>
#include <Adafruit_BMP280.h>

Adafruit_BMP280 bmp; //  to do: Verificat, inicializacion del objeto altímetro

float currentAltitude = 0; // Altura actual
float maxAltitude = -9999; // Altura max, apogeo

void setup() {
  Serial.begin(9600);
  
  if (!bmp.begin()) {
    Serial.println("No se pudo encontrar el altímetro, revise las conexiones! :(");
    while (1);
  }
}

void loop() {
  float newAltitude = bmp.readAltitude();
  checkAltitudeChange(newAltitude);
  checkMaxAltitude(newAltitude);
  currentAltitude = newAltitude;
  delay(1000);
}

void checkAltitudeChange(float newAltitude) {
  if (newAltitude > currentAltitude) {
    printAltitudeChange("Up", newAltitude);
  } else if (newAltitude < currentAltitude) {
    printAltitudeChange("Down", newAltitude);
  }
}

void checkMaxAltitude(float newAltitude) {
  if (newAltitude > maxAltitude) {
    maxAltitude = newAltitude;
    Serial.print("High Altitude! Altitude: ");
    Serial.print(maxAltitude);
    Serial.println(" m");
  }
}

void printAltitudeChange(const char* direction, float altitude) {
  Serial.print(direction);
  Serial.print(": ");
  Serial.print(altitude);
  Serial.println(" m");
}

