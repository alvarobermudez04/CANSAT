import serial
import pandas as pd

# Configura el objeto Serial
try:
    ser = serial.Serial('COM3', 9600)  # Asegúrate de ajustar la velocidad de baudios según tu configuración
except serial.SerialException:
    print("No se puede abrir el puerto COM3. Asegúrate de que el dispositivo esté conectado correctamente.")
    exit()

# Crea un DataFrame vacío
columnas = ['TEAM_ID', 'MISSION_TIME', 'PACKET_COUNT', 'MODE', 'STATE', 'ALTITUDE',
            'AIR_SPEED', 'HS_DEPLOYED', 'PC_DEPLOYED', 'TEMPERATURE', 'VOLTAGE',
            'PRESSURE', 'GPS_TIME', 'GPS_ALTITUDE', 'GPS_LATITUDE', 'GPS_LONGITUDE',
            'GPS_SATS', 'TILT_X', 'TILT_Y', 'ROT_Z', 'CMD_ECHO']

df = pd.DataFrame(columns=columnas)

try:
    while True:
        # Lee la línea y la divide por comas para obtener una lista de variables
        variables = ser.readline().decode('utf-8').strip().split(',')

        # Añade la lista como una nueva fila al DataFrame
        df = pd.concat([df, pd.Series(variables, index=columnas).to_frame().T], ignore_index=True)

        # Imprime el DataFrame actualizado
        print(df)

except KeyboardInterrupt:
    # Maneja la interrupción del teclado (Ctrl+C) para cerrar el puerto serial
    ser.close()
    print("Puerto serial cerrado.")
except serial.SerialException:
    print("Se perdió la conexión con el dispositivo en el puerto COM3.")
    ser.close()
