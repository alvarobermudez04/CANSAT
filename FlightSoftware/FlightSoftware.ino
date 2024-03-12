#include <Wire.h>
#include <Adafruit_Sensor.h>
#include "Adafruit_BMP3XX.h"

#define SEALEVELPRESSURE_HPA (1013.25)

#define STANDBY 0
#define ASCENDING 1
#define FIRST_DESCEND 2
#define SECOND_DESCEND 3
#define THIRD_DESCEND 4
#define LANDED 5

int state = STANDBY;
float previousAltitude = 0;
float currentAltitude = 0;

#define SIMULATION_MODE false // Cambiar a true para usar modo de simulación

void setup() {
  Serial.begin(9600);
  while (!Serial);

  // Inicialización del sensor BMP380
  if (!bmp.begin_I2C()) {
    Serial.println("No se pudo encontrar el sensor BMP3, revisa la conexión!");
    while (1);
  }

  bmp.setTemperatureOversampling(BMP3_OVERSAMPLING_8X);
  bmp.setPressureOversampling(BMP3_OVERSAMPLING_4X);
  bmp.setIIRFilterCoeff(BMP3_IIR_FILTER_COEFF_3);
  bmp.setOutputDataRate(BMP3_ODR_50_HZ);
}

void loop() {
  if (SIMULATION_MODE) {
    // Leer valores simulados desde el puerto serial
    if (Serial.available() > 0) {
      currentAltitude = Serial.parseFloat();
      // Descartar el carácter de nueva línea
      Serial.read();
    }
  } else {
    // Leer altitud desde el sensor BMP380
    if (!bmp.performReading()) {
      Serial.println("Error al leer el sensor BMP380 :(");
      return;
    }
    currentAltitude = bmp.readAltitude(SEALEVELPRESSURE_HPA);
  }

  // Determinar el estado actual basado en la altitud
  switch (state) {
    case STANDBY:
      if (currentAltitude == 0) {
        state = ASCENDING;
      }
      break;

    case ASCENDING:
      if (currentAltitude > previousAltitude) {
        state = ASCENDING;
      } else {
        state = FIRST_DESCEND;
      }
      break;

    case FIRST_DESCEND:
      if (currentAltitude < previousAltitude && currentAltitude > 100) {
        // Activar comando heatshield
        state = SECOND_DESCEND;
      }
      break;

    case SECOND_DESCEND:
      if (currentAltitude < previousAltitude && currentAltitude <= 100) {
        // Activar comando parachute
        state = THIRD_DESCEND;
      }
      break;

    case THIRD_DESCEND:
      if (currentAltitude < previousAltitude && state == SECOND_DESCEND) {
        // Tercera caída
        state = LANDED;
      }
      break;

    case LANDED:
      if (currentAltitude == 0) {
        // Activar comando beacon
        // Fin del vuelo
      }
      break;
  }

  // Actualizar altitud anterior con la actual para la próxima iteración
  previousAltitude = currentAltitude;

  // Imprimir estado actual
  switch (state) {
    case STANDBY:
      Serial.println("Stand By");
      break;
    case ASCENDING:
      Serial.println("Ascending");
      break;
    case FIRST_DESCEND:
      Serial.println("First Descend");
      break;
    case SECOND_DESCEND:
      Serial.println("Second Descend");
      break;
    case THIRD_DESCEND:
      Serial.println("Third Descend");
      break;
    case LANDED:
      Serial.println("Landed");
      break;
  }

  delay(1000); // Esperar 1 segundo antes de la próxima iteración
}
