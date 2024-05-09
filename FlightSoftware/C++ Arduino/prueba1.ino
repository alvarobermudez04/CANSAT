#include <EEPROM.h>
#include <Servo.h>

// Definición de pines
#define LED_PIN 13
#define BUZZER_PIN 12
#define SERVO_PIN 9

// Altitud de despliegue del paracaídas
#define ALTITUD_DESPLIEGUE_PARACAIDAS 100

//states
#define STANDBY 0
#define ASCENDING 1
#define FIRST_DESCEND 2
#define SECOND_DESCEND 3
#define LANDED 4

int state = STANDBY;
String actualState = "Standby"; //to do: remove
int numOfDescending = 0; //to do: remove

#define SIMULATION_MODE true // Cambiar a true para usar modo de simulación
// Vector de alturas simuladas
float alturas2[] = {0,0,0,1,1,2,23,30,40,50,100, 150, 200, 250, 300, 350, 400, 450, 500,449,400,300,300,200,101,100,99,80,70,23,10,5,3,2,1,1,1,0};
float alturas[] = {0,1,20,30,40, 150, 200, 400, 500,300,300,200,100,80,5,3,1,0};

// Índice para recorrer el vector de alturas
int indiceAltura = 0;



//altimetro

float currentAltitude = 0; // Altura actual
float previousAltitude = 0;
float maxAltitude = -9999; // Altura max, apogeo

bool launched = false;
bool descending = false;
bool landed = false;

// Variables globales
Servo parachuteServo;

void setup() {
  pinMode(LED_PIN, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);

  parachuteServo.attach(SERVO_PIN);

  Serial.begin(9600);


  //PROTOCOLO DE RECUPERACIÖN
  // Leer la altitud almacenada en la EEPROM al inicio
  float altitudGuardada = readAltitude_memory();
  Serial.print("Altitud recuperada ");
  Serial.print(altitudGuardada);
  previousAltitude = altitudGuardada;
}

void loop() {

    //ENCENDER LED
    digitalWrite(LED_PIN, HIGH);
  
    bool collected = collectingDataProtocol();


    // Guardar la altitud actual en la EEPROM
    saveAltitude(currentAltitude);  
  
    identifyState();

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
      }
      break;
    
    case ASCENDING:
      checkAltitudeChange(currentAltitude);
      checkMaxAltitude();
      break;
    
    case FIRST_DESCEND:
      printAltitudeChange("FIRST_DESCEND", currentAltitude);
      if (currentAltitude <= 100) {       
        state = SECOND_DESCEND;
   		//activate HS 
        Serial.print("------turn servo----------");
        desplegarParacaidasHS();
      }else {
        //waiting 10s ??
      }
      break;

    case SECOND_DESCEND:
      printAltitudeChange("SECOND_DESCEND", currentAltitude);
      if (currentAltitude <= 1) { // to do: check 
        // Activar comando beacon
        // Fin del vuelo
        landed=true;
        state = LANDED;
        printAltitudeChange("Landed", currentAltitude);
        Serial.print(": Waiting to be recovered");
        activateRecoveryProtocol();
      }
      break;

    case LANDED:
      //waiting
      activateRecoveryProtocol();
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
    case LANDED:
      Serial.println("Landed");
      break;
  }

}

//verifica si la diferencia de altitudes entre la actual y la actual guardada
void checkAltitudeChange(float newAltitude) {
  float altitudeChange = newAltitude - previousAltitude;
  
  if (altitudeChange >= 1) {
      printAltitudeChange("Up", newAltitude);
      state = ASCENDING;
  }
  if (altitudeChange <= -1 ){
      printAltitudeChange("PUNTO Máximo", newAltitude);
      printAltitudeChange("Down", newAltitude);
      state = FIRST_DESCEND;
      //activate Container 
      Serial.print("------turn servo----------");
      desplegarParacaidasContainer();
  }
    // Cambio de altitud mayor a 1 metro
    //to do: que hacer en este caso
  
}

// Funcion de guardar en la EEPROM
void saveAltitude(float altitud) {
  int direccion = 0;
  EEPROM.put(direccion, altitud);
  Serial.println("Altitud guardada en la EEPROM");
}

// Funcion de leer de la EEPROM
float readAltitude_memory() {
  float altitud;
  int direccion = 0;
  EEPROM.get(direccion, altitud);
  Serial.print("Altitud leída desde la EEPROM: ");
  Serial.println(altitud);
  return altitud;
}

//Obtener e imprimir altitude
void getAltitude() {
  // En una aplicación real, aquí se obtendría la altitud de un sensor
  // En este ejemplo, se retorna un valor simulado

  Serial.print("High Altitude! Altitude: ");
  Serial.print(currentAltitude);
  Serial.println("m");

}

//verifica si la altitud actual es mayor que altura maxima guardada
// si es mayor: se actualiza
void checkMaxAltitude() {
  if (currentAltitude > maxAltitude) {
    maxAltitude = currentAltitude;
  }
}

void printAltitudeChange(const char* direction, float altitude) {
  Serial.print(direction);
  Serial.print(": ");
  Serial.print(altitude);
  Serial.println(" m");
}

//Activar buzzer para despliegue
void desplegarParacaidasContainer() {
  // Girar el servo para desplegar el paracaídas
  parachuteServo.write(100);  // Gira el servo a 90 grados (posición de despliegue)
}

//Activar buzzer para despliegue
void desplegarParacaidasHS() {
  // Girar el servo para desplegar el paracaídas
  parachuteServo.write(180);  // Gira el servo a 90 grados (posición de despliegue)
}

//to do : metodo
bool collectingDataProtocol(){
  //to do: bewtween simulation or not
  if (SIMULATION_MODE) {
      // Incrementar el índice de altura (ciclar al inicio del vector si alcanza el final)
      indiceAltura = (indiceAltura + 1) % (sizeof(alturas) / sizeof(alturas[0]));
      // Obtener la altitud actual
  	  currentAltitude = alturas[indiceAltura];
    } else {
      // Leer altitud desde el sensor BMP380
      /*if (!bmp.performReading()) {
        Serial.println("Error al leer el sensor BMP380 :(");
        return false; //to do: consultar return 
      }
      currentAltitude = bmp.readAltitude(SEALEVELPRESSURE_HPA);*/
    }

  return true;
}

//to do : metodo
void activateRecoveryProtocol(){
 // activate recovery protocol
 // Activar el buzzer
  digitalWrite(BUZZER_PIN, HIGH);
  delay(2000); // Sonar durante 1 segundo
  digitalWrite(BUZZER_PIN, LOW); // Apagar el buzzer
 //  save data


}

