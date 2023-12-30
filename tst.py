from customtkinter import *     #pip install customtkinter
from PIL import Image           #pip install PIL
from datetime import datetime
import serial                   #pip install pyserial
import pandas as pd             #pip install pandas

class InterfazApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GroundStation")

        # Configura el objeto Serial
        try:
            self.ser = serial.Serial('COM3', 9600)  # Asegúrate de ajustar la velocidad de baudios según tu configuración
        except serial.SerialException:
            print("No se puede abrir el puerto COM3. Asegúrate de que el dispositivo esté conectado correctamente.")
            exit()

        # Crea un DataFrame vacío
        self.columnas = ['TEAM_ID', 'MISSION_TIME', 'PACKET_COUNT', 'MODE', 'STATE', 'ALTITUDE',
                    'AIR_SPEED', 'HS_DEPLOYED', 'PC_DEPLOYED', 'TEMPERATURE', 'VOLTAGE',
                    'PRESSURE', 'GPS_TIME', 'GPS_ALTITUDE', 'GPS_LATITUDE', 'GPS_LONGITUDE',
                    'GPS_SATS', 'TILT_X', 'TILT_Y', 'ROT_Z', 'CMD_ECHO']

        self.df = pd.DataFrame(columns=self.columnas)

        # Variables para almacenar datos
        self.state = "not connected"
        self.Sent_packages = "0"
        self.Recieved_packages = "0"
        self.Last_command = "NA"
        self.UTH_time = "hh:mm:ss"
        self.Mission_time = "T hh:mm:ss"
        self.HeatShield = "Not Deployed"
        self.Parachute = "Not Deployed"
        self.Satelites = "0"
        self.GPS_time = "hh:mm:ss"
        self.GPS_latitude = "0"
        self.GPS_longitude = "0"
        self.GPS_altitude = "0"
        self.Speed = "0"
        self.Pressure = "0"
        self.Temperature = "0"
        self.WindSpeed = "0"
        self.Altitude = "0"
        self.Tilt_x = "0"
        self.Tilt_y = "0"
        self.Roll = "0"
        self.Voltage = "0"

        # Pantalla Inicial
        self.pantalla_inicial()
        
    def pantalla_inicial(self):
        # Limpiar la pantalla actual
        self.clear_screen()
        
        # Lista de colores
        self.color_fondo            = "#FAFAFA"
        self.color_frame            = "#0E1734"
        self.color_bordes_frames    = "#F68A2E"
        self.color_texto_blanco     = "#D9D9D9"
        self.color_texto_negro      = "#1A1A1A"

        # Configura fullsize y color de fondo
        self.root.configure(fg_color=self.color_fondo)
        self.root.after(0,lambda:self.root.state('zoomed'))
        
        # Crear un Frame para el titulo y los botones en el centro
        background_frame = CTkFrame(self.root)
        background_frame.place(relwidth=1,relheight=1)
        main_frame = CTkFrame(self.root, fg_color=self.color_frame,corner_radius=0)
        main_frame.place(relwidth=0.45,relheight=1)
        
        # Titulo
        CTkLabel(main_frame, text="Team #2075", font=("Helvetica", 16),text_color=self.color_texto_blanco).pack(pady=200)

        # Botones
        button_mission = self.custom_button(main_frame, "New Mission", self.pantalla_mission)
        button_mission.pack(pady=10)

        button_simulation = self.custom_button(main_frame, "Go to simulation", self.pantalla_simulation)
        button_simulation.pack(pady=10)

        img_size=150
        # Cargar las imágenes
        width = self.root.winfo_screenwidth()
        height = self.root.winfo_screenheight()

        self.fondo_inicio   = CTkImage(dark_image=Image.open("GroundStation\\fondo inicio.jpg"),size=(width,height))
        self.gia_logo       = CTkImage(dark_image=Image.open("GroundStation\gia logo.jpg"),    size=(img_size,img_size))
        self.cansat_logo    = CTkImage(dark_image=Image.open("GroundStation\cansat logo.png"), size=(img_size,img_size))
        self.team_logo      = CTkImage(dark_image=Image.open("GroundStation\\team logo.jpg"),  size=(img_size,img_size))

        # coloca las imagenes
        
        CTkLabel(background_frame, image=self.fondo_inicio, text="").place(relwidth=1, relheight=1)
        CTkLabel(main_frame, image=self.team_logo, text="").place(rely=0.7,relx=0.375*2-0.02)
        CTkLabel(main_frame, image=self.gia_logo, text="").place(rely=0.7,relx=0.02)
        CTkLabel(main_frame, image=self.cansat_logo, text="").place(rely=0.7,relx=0.375)
        
    def pantalla_mission(self):       
        # Limpiar la pantalla actual
        self.clear_screen()

        # Frames
        self.left_frame = CTkFrame(self.root, fg_color=self.color_frame)
        self.left_frame.place(relwidth=0.26,relheight=1)
        
        self.center_frame = CTkFrame(self.root, fg_color=self.color_texto_blanco, 
                                    border_color=self.color_bordes_frames,border_width=4,corner_radius=20)
        self.center_frame.place(relx=0.28, rely=0.02,relwidth=0.38,relheight=0.32)
        
        self.right_frame = CTkFrame(self.root, fg_color=self.color_texto_blanco, 
                                    border_color=self.color_bordes_frames,border_width=4,corner_radius=20)
        self.right_frame.place(relx=0.68, rely=0.02,relwidth=0.3,relheight=0.32)

        self.bottom_frame = CTkFrame(self.root, fg_color=self.color_texto_blanco, 
                                    border_color=self.color_bordes_frames,border_width=4,corner_radius=20)  
        self.bottom_frame.place(relx=0.28, rely=0.37,relwidth=0.7,relheight=0.6)

        self.white_top_frame = CTkFrame(self.bottom_frame, fg_color="white", corner_radius=20)  
        self.white_top_frame.place(relx=0.5, rely=0.02,relwidth=0.48,relheight=0.47)

        self.white_bottom_frame = CTkFrame(self.bottom_frame, fg_color="white", corner_radius=20)  
        self.white_bottom_frame.place(relx=0.5, rely=0.51,relwidth=0.48,relheight=0.47)

        # Imagen logo
        self.team_logo_big      = CTkImage(dark_image=Image.open("GroundStation\\team logo.jpg"),  size=(200,200))
        CTkLabel(self.left_frame, image=self.team_logo_big, text="").pack(pady=10)

        # Titulo y textos
        CTkLabel(self.left_frame, text="Team #2075"  , font=("Helvetica", 30,"bold"),
                 text_color=self.color_texto_blanco).pack(pady=20)
        CTkLabel(self.center_frame, text="Indicators", font=("Helvetica", 35,"bold"),
                 text_color=self.color_texto_negro).place(relx=0.05,rely=0.05)
        CTkLabel(self.right_frame , text="Commands"  , font=("Helvetica", 30,"bold"),
                 text_color=self.color_texto_negro).place(relx=0.05,rely=0.05)
        CTkLabel(self.bottom_frame, text="Data"      , font=("Helvetica", 30,"bold"),
                 text_color=self.color_texto_negro).place(relx=0.05,rely=0.05)

        self.left_label         = CTkLabel(self.left_frame, 
                                    text=
                                        "UTC Time: "+ '\n'+
                                        "Mission time: "        + '\n'+
                                        "State"                 + '\n'+
                                        "Sent packages: "       + '\n'+
                                        "Recieved packages: "   + '\n'+  
                                        "Last Command: ", 
                                    justify=LEFT,
                                    font=("Helvetica", 20),                                                   
                                    text_color=self.color_texto_blanco)
    
        self.satelites_label    = CTkLabel(self.bottom_frame, 
                                    text=
                                        "Satelites conected: "+ '\n'+
                                        "GPS Time: "     ,
                                    justify=LEFT,
                                    font=("Helvetica", 30),
                                    text_color=self.color_texto_negro)
                                                   
        self.white_top_label    = CTkLabel(self.white_top_frame, 
                                    text=
                                        "Speed: "       + '\n'+
                                        "Temperature: " + '\n'+
                                        "Pressure: "    + '\n'+
                                        "Wind Speed: ", 
                                    font=("Helvetica", 20),
                                    text_color=self.color_texto_negro)
        
        self.white_bottom_label = CTkLabel(self.white_bottom_frame, 
                                    text=
                                        "Altitude: "    + '\n'+
                                        "Tilt: "        + '\n'+
                                        "Roll: "        + '\n'+
                                        "Voltage: ", 
                                    font=("Helvetica", 20),
                                    text_color=self.color_texto_negro)
        
        self.left_label.pack(pady=10)
        self.satelites_label.place(relx=0.1,rely=0.8)
        self.white_top_label.pack(pady=70)
        self.white_bottom_label.pack(pady=70)
        
        # Switches para la telemetria
        switch_var_telemetry   = StringVar(value="off")
        switch_var_heatshield  = StringVar(value="off")
        switch_var_parachute   = StringVar(value="off")
        switch_var_audiobeacon = StringVar(value="off")

        self.start_telemetry_switch   = CTkSwitch(self.center_frame, 
                                                text="Start telemetry",
                                                progress_color="#3DBA50",
                                                command=self.telemetry_on,
                                                variable=switch_var_telemetry, 
                                                onvalue="on",
                                                offvalue="off",
                                                font=("Helvetica", 30),
                                                text_color=self.color_texto_negro).place(relx=0.05,rely=0.35)
        
        self.start_heatshield_switch  = CTkSwitch(self.center_frame, 
                                                text="Heatshield",
                                                progress_color="#3DBA50",
                                                command=self.heatshield_on,
                                                variable=switch_var_heatshield, 
                                                onvalue="on",
                                                offvalue="off",
                                                font=("Helvetica", 30),
                                                text_color=self.color_texto_negro).place(relx=0.05,rely=0.5)
        
        self.start_parachute_switch   = CTkSwitch(self.center_frame, 
                                                text="Parachute",
                                                progress_color="#3DBA50",
                                                command=self.parachute_on,
                                                variable=switch_var_parachute, 
                                                onvalue="on",
                                                offvalue="off",
                                                font=("Helvetica", 30),
                                                text_color=self.color_texto_negro).place(relx=0.05,rely=0.65)
        
        self.start_audiobeacon_switch = CTkSwitch(self.center_frame, 
                                                text="Audiobeacon",
                                                progress_color="#3DBA50",
                                                command=self.audiobeacon_on,
                                                variable=switch_var_audiobeacon, 
                                                onvalue="on",
                                                offvalue="off",
                                                font=("Helvetica", 30),
                                                text_color=self.color_texto_negro).place(relx=0.05,rely=0.8)

        # Command buttons
        calibrate_altitude_button = self.custom_button(self.right_frame, "Calibrate Altitude", self.calibrate_altitude)
        calibrate_altitude_button.place(relx=0.05,rely=0.3)

        set_time_button = self.custom_button(self.right_frame, "Set time", self.set_time)
        set_time_button.place(relx=0.05,rely=0.5)

        save_and_export_button = self.custom_button(self.right_frame, "Save and export", self.save_and_export)
        save_and_export_button.place(relx=0.05,rely=0.7)

        # Botón de regresar
        backbutton = self.custom_button(self.left_frame, "Return", self.pantalla_inicial)
        backbutton.place(relx=0.2,rely=0.9)

        self.actualizar_contenido()


        

    def telemetry_on(self):
        pass

    def heatshield_on(self):
        pass
    
    def parachute_on(self):
        pass
    
    def audiobeacon_on(self):
        pass

    def calibrate_altitude(self):
        pass

    def set_time(self):
        pass

    def save_and_export(self):
        pass
    
    def actualizar_contenido(self):
        
        # Actualiza las variables con los datos del puerto serie
        ser = self.ser
        try:
            # Lee la línea y la divide por comas para obtener una lista de variables
            self.variables = ser.readline().decode('utf-8').strip().split(',')
            self.df = pd.concat([self.df, pd.Series(self.variables, index=self.columnas).to_frame().T], ignore_index=True)

            # Actualiza las variables de la clase
            self.UTH_time = datetime.utcnow().strftime('%H:%M:%S')
            self.Sent_packages = self.variables[2]
            self.Recieved_packages = str(len(self.df))
            self.state = self.variables[4]
            self.Altitude = self.variables[5]
            self.WindSpeed = self.variables[6]
            self.Temperature = self.variables[9]
            self.Voltage = self.variables[10]
            self.Pressure = self.variables[11]
            self.GPS_time = self.variables[12]
            self.GPS_altitude = self.variables[13]
            self.GPS_latitude = self.variables[14]
            self.GPS_longitude = self.variables[15]
            self.Satelites = self.variables[16]
            self.Tilt_x = self.variables[17]
            self.Tilt_y = self.variables[18]
            self.Roll = self.variables[19]
            self.Last_command = self.variables[20]
            # ... (actualizar otras variables según sea necesario)

            

        except Exception as e:
            print(f"Error al leer desde el puerto serie: {e}")

        # Actualizar labels
        self.left_label.configure(text= 
                                    "UTC Time: "            + self.UTH_time +'\n'+
                                    "Mission time: "        + self.Mission_time+'\n'+
                                    "State: "               + self.state+'\n'+
                                    "Sent packages: "       + self.Sent_packages+'\n'+
                                    "Recieved packages: "   + self.Recieved_packages+'\n'+
                                    "Last Command: "        + self.Last_command)
    
        self.satelites_label.configure(text=
                                    "Satelites conected: "  + self.Satelites+'\n'+
                                    "GPS Time: "            + self.GPS_time)
        
        self.white_top_label.configure(text=
                                    "Speed: "               + self.Speed        +' m/s\n'+
                                    "Temperature: "         + self.Temperature  +' °C\n'+
                                    "Pressure: "            + self.Pressure     +' kPa\n'+
                                    "Wind Speed: "          + self.WindSpeed    +' m/s')
        
        self.white_bottom_label.configure(text=
                                    "Altitude: "            + self.Altitude     +' m\n'+
                                    "Tilt: "                + self.Tilt_x       +' °\n'+
                                    "Roll: "                + self.Roll         +' °/s\n'+
                                    "Voltage: "             + self.Voltage      +' m/s')
        
        # Llamar a la función después de 1000 milisegundos (1 segundo)
        self.root.after(1000, self.actualizar_contenido)
        

    def pantalla_simulation(self):
        # Limpiar la pantalla actual
        self.clear_screen()

        CTkLabel(self.root, text="Simulation Mode", font=("Helvetica", 16)).pack(pady=20)

        


        # Botón de regresar
        backbutton = self.custom_button(self.root, "Return", self.pantalla_inicial)
        backbutton.pack(pady=10)
    
    def clear_screen(self):
        # Limpiar la pantalla
        for widget in self.root.winfo_children():
            widget.destroy()

    def custom_button(self, lugar, texto, comando):
        # Configuracion de los botones
        return CTkButton(lugar, text=texto, command=comando,
        width=250, 
        height=50, 
        corner_radius=30,
        fg_color=self.color_frame,
        font=("Helvetica", 20),
        border_width=3,
        border_color=self.color_bordes_frames,
        hover_color="#243B86")

if __name__ == "__main__":
    root = CTk()
    app = InterfazApp(root)
    root.mainloop()