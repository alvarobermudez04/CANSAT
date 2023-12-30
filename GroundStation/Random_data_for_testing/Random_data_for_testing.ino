#include <Wire.h>

void setup() {
  Serial.begin(9600);
  randomSeed(analogRead(0));  // Inicializar la semilla para generar números aleatorios
}

void loop() {
  // Valores ficticios para cada campo
  int TEAM_ID = 2075;
  String MISSION_TIME = "12:00:00";
  static int PACKET_COUNT = 1;
  String MODE = "F";
  String STATE = "Arduino_connected";
  float ALTITUDE = 10.1;
  float AIR_SPEED = 5.5;
  String HS_DEPLOYED = "N";
  String PC_DEPLOYED = "N";
  float TEMPERATURE = 25.0;
  float VOLTAGE = 12.0;
  float PRESSURE = 101.325;
  String GPS_TIME = "12:34:56";
  float GPS_ALTITUDE = 10.7;
  float GPS_LATITUDE = 9.920901;
  float GPS_LONGITUDE = -84.056108;
  int GPS_SATS = 8;
  float TILT_X = 1.0;
  float TILT_Y = 2.0;
  float ROT_Z = 3.0;
  String CMD_ECHO = "CMD2075CXOFF";

  // Generar un número aleatorio entre 0 y 9
  int randomValue = random(10);

  // Imprimir el string formateado solo si el número aleatorio es menor que 5 (50% de probabilidad)
  if (randomValue < 9) {
    Serial.print(TEAM_ID);
    Serial.print(',');
    Serial.print(MISSION_TIME);
    Serial.print(',');
    Serial.print(PACKET_COUNT);
    Serial.print(',');
    Serial.print(MODE);
    Serial.print(',');
    Serial.print(STATE);
    Serial.print(',');
    Serial.print(ALTITUDE);
    Serial.print(',');
    Serial.print(AIR_SPEED);
    Serial.print(',');
    Serial.print(HS_DEPLOYED);
    Serial.print(',');
    Serial.print(PC_DEPLOYED);
    Serial.print(',');
    Serial.print(TEMPERATURE);
    Serial.print(',');
    Serial.print(VOLTAGE);
    Serial.print(',');
    Serial.print(PRESSURE);
    Serial.print(',');
    Serial.print(GPS_TIME);
    Serial.print(',');
    Serial.print(GPS_ALTITUDE);
    Serial.print(',');
    Serial.print(GPS_LATITUDE);
    Serial.print(',');
    Serial.print(GPS_LONGITUDE);
    Serial.print(',');
    Serial.print(GPS_SATS);
    Serial.print(',');
    Serial.print(TILT_X);
    Serial.print(',');
    Serial.print(TILT_Y);
    Serial.print(',');
    Serial.print(ROT_Z);
    Serial.print(',');
    Serial.print(CMD_ECHO);
    Serial.println(); // Nueva línea al final del string

    
  }
  PACKET_COUNT++; // Incrementar PACKET_COUNT solo si se imprime un paquete
  delay(1000); // Esperar un segundo
}
