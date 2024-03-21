#include <Wire.h>
#include <Adafruit_BMP280.h>

Adafruit_BMP280 bmp; //  to do: Verificat, inicializacion del objeto altímetro

float currentAltitude = 0; // Altura actual
float maxAltitude = -9999; // Altura max, apogeo
bool launched = false;
bool landed = false;
String actualState = "Started";
bool descending = false;
int numOfDescending = 0;



void setup() {
  Serial.begin(9600); //to do: verificar serial
  
  if (!bmp.begin()) {
    Serial.println("Could not find altimeter, check connections! :(");
    while (1);
  }
}

// metodo loop
void loop() {
  float newAltitude = bmp.readAltitude();
  identifyState(newAltitude);
  currentAltitude = newAltitude;
  delay(1000);
}

void identifyState(float newAltitude){
  if (newAltitude == 0){
    //verificar si el estado es esperando por ser lanzado o ya 
    if (launched == false ){
      actualState="Started";
      Serial.print(actualState);
      Serial.print(": Waiting for launch");
      //to do: esperar 1s
      
    }
    if (landed == true){
      actualState="Landed";
      Serial.print(actualState);
      Serial.print(": Waiting to be recovered");
      //to do: esperar 1s
    }
  }else{
    if (launched == false){launched=true;actualState="Ascending";}// ya fue lanzado
    checkAltitudeChange(newAltitude);
  }

}


//verifica si la altitud actual es mayor que la actual guardada
// si es mayor: esta subiendo
// si es menor: esta bajando 
/*void checkAltitudeChange(float newAltitude) {
  if (newAltitude > currentAltitude) {
    printAltitudeChange("Up", newAltitude);
  } else if (newAltitude < currentAltitude) {
    printAltitudeChange("Down", newAltitude);
  }
}*/

//verifica si la diferencia de altitudes entre la actual y la actual guardada
// 
void checkAltitudeChange(float newAltitude) {
  float altitudeChange = newAltitude - currentAltitude;
  
  switch (int(altitudeChange)) {
    case 0:
      break; // No hay cambio de altitud
    case 1:
      printAltitudeChange("Up", newAltitude);
      actualState="Ascending";
      collectingDataProtocol();
      Serial.print(actualState);
      break;
    case -1:
      printAltitudeChange("Down", newAltitude);
      descending(newAltitude);
      Serial.print(actualState);
      break;
    default:
      break; // Cambio de altitud mayor a 1 metro
      //to do: que hacer en este caso
  }
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

//verificar la etapa de descenso
void descending(float newAltitude){
  if (descending == false){descending=true;actualState="First Descending";numOfDescending=1;}// ya va descendiendo
  
  if (newAltitude >= 100 ){
    //esta en el primer descenso
    collectingDataProtocol();
    //esperaar luego del apoger hasta 5m

  
  } else {
    //to do: identificar la diferencia desde el arduino entre el segundo y tercer descenso

    //segundo descenso
    numOfDescending=2;
    actualState="Second Descending";
    collectingDataProtocol();
    //active HS, primer paracaidas, abrir paracaidas
    //activar HS

    // tercer descenso
    // numOfDescending=3;
    // actualState="Thrird Descending";
    // to do
    //es justo en 100
    //activar PC


    //verificar si ya aterrizó
    if (newAltitude == 0 && launched == true){
      actualState="Landed";
      landed=true;
      activateRecoveryProtocol();
    }
  }
}

//to do : metodo
void collectingDataProtocol(){
  //get data sensors
  //save altitude
  //convert data
  //save to memory
  //send as data protocol
  //wait 1s
}

//to do : metodo
void activateRecoveryProtocol(){¿
 // stop collecting data and tranfer
 //  save data
 // activate recovery protocol
}
