#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BMP280.h> // to do: revisar sensor


#define SEALEVELPRESSURE_HPA (1013.25)

#define STANDBY 0
#define ASCENDING 1
#define FIRST_DESCEND 2
#define SECOND_DESCEND 3
#define THIRD_DESCEND 4
#define LANDED 5

int state = STANDBY;
String actualState = "Standby"; //to do: remove
int numOfDescending = 0; //to do: remove


#define SIMULATION_MODE false // Cambiar a true para usar modo de simulación


Adafruit_BMP280 bmp; //  to do: Verificat, inicializacion del objeto altímetro

float currentAltitude = 0; // Altura actual
float previousAltitude = 0;
float maxAltitude = -9999; // Altura max, apogeo

bool launched = false;
bool descending = false;
bool landed = false;


void setup() {
  Serial.begin(9600); //to do: verificar serial
  while (!Serial);
  
  // Inicialización del sensor BMP380
  if (!bmp.begin()) {
    Serial.println("Could not find altimeter, check connections! :(");
    while (1);
  }

  //consultar *************** 
  bmp.setTemperatureOversampling(BMP3_OVERSAMPLING_8X);
  bmp.setPressureOversampling(BMP3_OVERSAMPLING_4X);
  bmp.setIIRFilterCoeff(BMP3_IIR_FILTER_COEFF_3);
  bmp.setOutputDataRate(BMP3_ODR_50_HZ);
}

// metodo loop
void loop() {
  bool collected = collectingDataProtocol();

  if (collected == True){
    // to do: check this
  }

  identifyState(currentAltitude);
  previousAltitude=currentAltitude;

  delay(1000);
}

void identifyState(){
 // Determinar el estado actual basado en la altitud
  switch (state) {
    case STANDBY:
    //verificar si el estado es esperando por ser lanzado o ya 
      if ( 2 < currentAltitude ) { //2 metros
        state = ASCENDING;
        Serial.print("Ascending");
        Serial.print(": Start derecting that was launched");
        launched=true;
      } else {
        Serial.print("Stanby");
        Serial.print(": Waiting for launch");
        //to do: esperar 1s
      }
      break;
    
    case ASCENDING:
      checkAltitudeChange(currentAltitude);
      break;
    
    case FIRST_DESCEND:
      //waiting to be at 750m 
      if (currentAltitude < previousAltitude && currentAltitude > 750) {       
        state = SECOND_DESCEND;
        //activate HS

      }else {
        //waiting 10s ??
      }
      break;

    case SECOND_DESCEND:
      if (currentAltitude < previousAltitude && currentAltitude <= 100) {
        // Activate parachute
        state = THIRD_DESCEND;
      }else {
        //waiting to be at 100m
      }
      break;

    case THIRD_DESCEND:
      if (currentAltitude <= 1) { // to do: check 
      // Activar comando beacon
      // Fin del vuelo
      landed=true;
      state = LANDED;
      Serial.print("Landed");
      Serial.print(": Waiting to be recovered");
      activateRecoveryProtocol();
      }
    break;

    case LANDED:
      // ti do: what?
    break;
  }

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


//verifica si la diferencia de altitudes entre la actual y la actual guardada
// 
void checkAltitudeChange(float newAltitude) {
  float altitudeChange = newAltitude - currentAltitude;
  the_state = "";
  
  if (altitudeChange == 1) {
      printAltitudeChange("Up", newAltitude);
      state = ASCENDING;
  }
  if (altitudeChange == -1 ){
      printAltitudeChange("Down", newAltitude);
      state = FIRST_DESCEND;
  }
    // Cambio de altitud mayor a 1 metro
    //to do: que hacer en este caso
  
}

//verifica si la altitud actual es mayor que altura maxima guardada
// si es mayor: se actualiza
void checkMaxAltitude(float newAltitude) {
  if (newAltitude > maxAltitude) {
    maxAltitude = newAltitude;
   /*Serial.print("High Altitude! Altitude: ");
    Serial.print(maxAltitude);
    Serial.println(" m");*/
  }
}

void printAltitudeChange(const char* direction, float altitude) {
  Serial.print(direction);
  Serial.print(": ");
  Serial.print(altitude);
  Serial.println(" m");
}

//to do : metodo
bool collectingDataProtocol(){
  //to do: bewtween simulation or not
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
        return false; //to do: consultar return 
      }
      currentAltitude = bmp.readAltitude(SEALEVELPRESSURE_HPA);
    }

  //get data sensors
  //save altitude
  //convert data
  //save to memory
  //send as data protocol
  //wait 1s
  return true;
}

//to do : metodo
void activateRecoveryProtocol(){¿
 // stop collecting data and tranfer
 //  save data
 // activate recovery protocol
}
