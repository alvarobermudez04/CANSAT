import time
import machine
import utime

# Definición de constantes
SEALEVELPRESSURE_HPA = 1013.25

STANDBY = 0
ASCENDING = 1
FIRST_DESCEND = 2
SECOND_DESCEND = 3
THIRD_DESCEND = 4
LANDED = 5

# Inicialización del sensor BMP280
i2c = machine.I2C(0)
bmp280 = bmp280.BMP280(i2c)

# Inicialización de variables
state = STANDBY
launched = False
descending = False
landed = False
previous_altitude = 0
max_altitude = -9999
current_altitude = 0

def identify_state(current_altitude):
    global state
    global launched
    global descending
    global landed
    global previous_altitude
    global max_altitude
    
    # Determinar el estado actual basado en la altitud
    if state == STANDBY:
        if current_altitude > 2:
            state = ASCENDING
            launched = True
    elif state == ASCENDING:
        if current_altitude < previous_altitude:
            state = FIRST_DESCEND
    elif state == FIRST_DESCEND:
        if current_altitude < previous_altitude and current_altitude > 750:
            state = SECOND_DESCEND
    elif state == SECOND_DESCEND:
        if current_altitude < previous_altitude and current_altitude <= 100:
            state = THIRD_DESCEND
    elif state == THIRD_DESCEND:
        if current_altitude <= 1:
            state = LANDED
            landed = True
            activate_recovery_protocol()
    
    # Actualizar la altitud máxima
    if current_altitude > max_altitude:
        max_altitude = current_altitude
    
    previous_altitude = current_altitude

def check_altitude_change(new_altitude):
    global state
    
    altitude_change = new_altitude - previous_altitude
    
    if altitude_change == 1:
        state = ASCENDING
    elif altitude_change == -1:
        state = FIRST_DESCEND

def collecting_data_protocol():
    global launched
    global descending
    global landed
    
    if launched:
        # Leer altitud desde el sensor BMP280
        current_altitude = bmp280.altitude(SEALEVELPRESSURE_HPA)
        
        # Recopilar datos, guardar en memoria, enviar como protocolo de datos, etc.
        # Hacer algo con la altitud actual
        
        # Simulación de espera
        utime.sleep(1)
        
        return True
    
    return False

def activate_recovery_protocol():
    # Detener la recopilación de datos y transferir
    # Guardar datos
    # Activar el protocolo de recuperación
    pass


# Bucle principal
while True:
    # Protocolo de recopilación de datos
    collected = collecting_data_protocol()
    
    if collected:
        # Procesar datos y actualizar estado
        identify_state(current_altitude)
        
        # Verificar cambio de altitud
        check_altitude_change(current_altitude)
        
    time.sleep(1)  # Esperar 1 segundo antes de la próxima iteración
