from customtkinter import *     #pip install customtkinter
from customtkinter import filedialog
from PIL import Image,ImageDraw           #pip install PIL
from datetime import datetime
import serial                   #pip install pyserial
import pandas as pd             #pip install pandas
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.gridspec import GridSpec
import threading
import time
import random

class InterfazApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GroundStation")

        # Configura el objeto Serial
        try:
            self.ser = serial.Serial('COM3', 9600)  # Asegúrate de ajustar la velocidad de baudios según tu configuración
        except serial.SerialException:
            print("No se puede abrir el puerto COM3. Asegúrate de que el dispositivo esté conectado correctamente.")
            #exit()

        # Crea un DataFrame vacío
        self.columnas = ['TEAM_ID', 'MISSION_TIME', 'PACKET_COUNT', 'MODE', 'STATE', 'ALTITUDE',
                    'AIR_SPEED', 'HS_DEPLOYED', 'PC_DEPLOYED', 'TEMPERATURE', 'VOLTAGE',
                    'PRESSURE', 'GPS_TIME', 'GPS_ALTITUDE', 'GPS_LATITUDE', 'GPS_LONGITUDE',
                    'GPS_SATS', 'TILT_X', 'TILT_Y', 'ROT_Z', 'CMD', '2075','Last command','Data']

        self.df = pd.DataFrame(columns=self.columnas)

        # Variables para almacenar datos
        self.state = "not connected"
        self.Sent_packages = "0"
        self.Recieved_packages = "0"
        self.Last_command = "NA"
        self.Last_data = "NA"
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
        #para cronometro de graficos
        self.inicio_tiempo = 0

        # Inicializar listas para almacenar datos de cada gráfico
        self.datos_grafico1 = []
        self.datos_grafico2 = []
        self.datos_grafico3 = []
        self.datos_grafico4 = []
        self.datos_grafico5 = []
        self.datos_grafico6 = []
        self.datos_grafico7 = []


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
        CTkLabel(main_frame, text="Team #2075" + '\n'+"Ground Station", 
                 font=("Helvetica", 30),text_color=self.color_texto_blanco).place(relx=0.35,rely=0.27)

        # Botones
        button_mission = self.custom_button(main_frame, "New Mission", self.pantalla_mission)
        button_mission.place(relx=0.33,rely=0.4)

        button_simulation = self.custom_button(main_frame, "Go to simulation", self.pantalla_simulation)
        button_simulation.place(relx=0.33,rely=0.5)

        # Cargar las imágenes
        width = self.root.winfo_screenwidth()
        height = self.root.winfo_screenheight()
        
        def round_corners(image_path, corner_radius):
            original_image = Image.open(image_path)
            rounded_image = Image.new("RGBA", original_image.size, (0, 0, 0, 0))
            mask = Image.new("L", original_image.size, 0)
            draw = ImageDraw.Draw(mask)
            draw.rounded_rectangle([0, 0, original_image.width, original_image.height], corner_radius, fill=255)
            rounded_image.paste(original_image, (0, 0), mask)
            return rounded_image

        # Crear imágenes redondeadas
        rounded_gia = round_corners(r"GroundStation\gia logo.jpg", 200)
        rounded_cansat = round_corners(r"GroundStation\CanSat logo.png", 60)
        self.rounded_team = round_corners(r"GroundStation\team logo.jpg", 50)
        rounded_ucr = round_corners(r"GroundStation\ucr logo.jpg", 100)

        self.fondo_inicio   = CTkImage(dark_image=Image.open("GroundStation\\fondo inicio.jpg"), size=(width, height))
        self.gia_logo       = CTkImage(dark_image=rounded_gia, size=(150, 150))
        self.cansat_logo    = CTkImage(dark_image=rounded_cansat, size=(150, 150))
        self.team_logo      = CTkImage(dark_image=self.rounded_team, size=(150, 150))
        self.ucr_logo       = CTkImage(dark_image=rounded_ucr, size=(150, 150))

        # coloca las imagenes
        CTkLabel(background_frame, image=self.fondo_inicio, text="").place(relwidth=1, relheight=1)
        CTkLabel(main_frame, image=self.ucr_logo, text="",corner_radius=20).place(rely=0.7,relx=0.35*2-0.03)
        CTkLabel(main_frame, image=self.gia_logo, text="").place(rely=0.7,relx=0.11)
        CTkLabel(main_frame, image=self.cansat_logo, text="").place(rely=0.7,relx=0.4)
        CTkLabel(main_frame, image=self.team_logo, text= "").place(rely=0.05,relx=0.4)

    def pantalla_mission(self):
        self.set_up()
        self.team_label.configure(text="Team #2075" + '\n'+"Flight mode")

        save_and_export_button = self.custom_button(self.top_right_frame, "Save and export", self.save_and_export)
        save_and_export_button.place(relx=0.05,rely=0.7)

        self.switch_var_heatshield  = StringVar(value="off")
        self.switch_var_parachute   = StringVar(value="off")
        self.switch_var_audiobeacon = StringVar(value="off")

        self.start_heatshield_switch  = CTkSwitch(self.top_center_frame, 
                                                text="Heatshield",
                                                progress_color="#3DBA50",
                                                command=self.heatshield_on,
                                                variable=self.switch_var_heatshield, 
                                                onvalue="on",
                                                offvalue="off",
                                                font=("Helvetica", 30),
                                                text_color=self.color_texto_negro).place(relx=0.05,rely=0.5)
        
        self.start_parachute_switch   = CTkSwitch(self.top_center_frame, 
                                                text="Parachute",
                                                progress_color="#3DBA50",
                                                command=self.parachute_on,
                                                variable=self.switch_var_parachute, 
                                                onvalue="on",
                                                offvalue="off",
                                                font=("Helvetica", 30),
                                                text_color=self.color_texto_negro).place(relx=0.05,rely=0.65)
        
        self.start_audiobeacon_switch = CTkSwitch(self.top_center_frame, 
                                                text="Audiobeacon",
                                                progress_color="#3DBA50",
                                                command=self.audiobeacon_on,
                                                variable=self.switch_var_audiobeacon, 
                                                onvalue="on",
                                                offvalue="off",
                                                font=("Helvetica", 30),
                                                text_color=self.color_texto_negro).place(relx=0.05,rely=0.8)

    def pantalla_simulation(self):
        # Limpiar la pantalla actual
        self.set_up()
        self.team_label.configure(text="Team #2075" + '\n'+"Simulation mode")

        read_and_import_button = self.custom_button(self.top_right_frame, "Open simulation file", self.read_and_import)
        read_and_import_button.place(relx=0.05,rely=0.7)

        self.switch_var_simulation = StringVar(value="off")

        self.start_simulation_switch  = CTkSwitch(self.top_center_frame, 
                                                text="Simulation activate",
                                                progress_color="#3DBA50",
                                                command=self.simulation_on,
                                                variable=self.switch_var_simulation, 
                                                onvalue="on",
                                                offvalue="off",
                                                font=("Helvetica", 30),
                                                text_color=self.color_texto_negro).place(relx=0.05,rely=0.5)
        
    def set_up(self):
        # Limpiar la pantalla actual
        self.clear_screen()
        # Inicializar el tiempo de inicio cronometro para graficos
        self.inicio_tiempo = time.time()

        # Frames
        self.left_frame = CTkFrame(self.root, fg_color=self.color_frame,corner_radius=0)
        self.right = CTkFrame(self.root, fg_color=self.color_frame,corner_radius=0)
        self.white_right = CTkFrame(self.right, fg_color="white",corner_radius=20)
        self.top_center_frame = CTkFrame(self.root, fg_color=self.color_texto_blanco, 
                                    border_color=self.color_bordes_frames,border_width=4,corner_radius=20)
        self.top_right_frame = CTkFrame(self.root, fg_color=self.color_texto_blanco, 
                                    border_color=self.color_bordes_frames,border_width=4,corner_radius=20)
        self.bottom_frame = CTkFrame(self.root, fg_color=self.color_texto_blanco, 
                                    border_color=self.color_bordes_frames,border_width=4,corner_radius=20)  
        self.white_gps_frame = CTkFrame(self.bottom_frame, fg_color="white", corner_radius=20)  
        self.white_graphics_frame = CTkFrame(self.bottom_frame, fg_color="white", corner_radius=20)  
        self.white_data_frame = CTkFrame(self.bottom_frame, fg_color="white", corner_radius=20)  

        # Colocacion de los frames
        self.left_frame.place(relwidth=0.26,relheight=1)
        self.right.place(relx=0.81,relwidth=0.19,relheight=1)
        self.white_right.place(relx=0.05,rely=0.01,relwidth=0.9,relheight=0.98)
        self.top_center_frame.place(relx=0.27, rely=0.01,relwidth=0.26,relheight=0.30)
        self.top_right_frame.place(relx=0.54, rely=0.01,relwidth=0.26,relheight=0.30)
        self.bottom_frame.place(relx=0.27, rely=0.32,relwidth=0.53,relheight=0.66)
        self.white_gps_frame.place(relx=0.02, rely=0.02,relwidth=0.4,relheight=0.6)
        self.white_graphics_frame.place(relx=0.44, rely=0.02,relwidth=0.54,relheight=0.95)
        self.white_data_frame.place(relx=0.02, rely=0.64,relwidth=0.4,relheight=0.33)

        # Imagen logo
        self.team_logo_big      = CTkImage(dark_image=self.rounded_team, size=(200, 200))
        CTkLabel(self.left_frame, image=self.team_logo_big, text="").pack(pady=10)

        # Titulo y textos
        self.team_label = CTkLabel(self.left_frame, text="" , font=("Helvetica", 30,"bold"),
                 text_color=self.color_texto_blanco)
        self.team_label.pack(pady=20)
        CTkLabel(self.top_center_frame, text="Indicators", font=("Helvetica", 30,"bold"),
                 text_color=self.color_texto_negro).place(relx=0.05,rely=0.05)
        CTkLabel(self.top_right_frame , text="Commands"  , font=("Helvetica", 30,"bold"),
                 text_color=self.color_texto_negro).place(relx=0.05,rely=0.05)
        CTkLabel(self.white_gps_frame, text="GPS position", font=("Helvetica", 30,"bold"),
                 text_color=self.color_texto_negro).place(relx=0.1,rely=0.03)

        self.left_label         = CTkLabel(self.left_frame, 
                                    text=
                                        "UTC Time: \n"+
                                        "Mission time: \n"+
                                        "State: \n"+
                                        "Sent packages: \n"+
                                        "Recieved packages: ", 
                                    justify=LEFT,
                                    font=("Helvetica", 30),                                                   
                                    text_color=self.color_texto_blanco)
    
        self.satelites_label    = CTkLabel(self.white_gps_frame, 
                                    text=
                                        "Satelites conected: \n"+
                                        "GPS Time: "     ,
                                    justify=LEFT,
                                    font=("Helvetica", 26),
                                    text_color=self.color_texto_negro)
        
        #seccion de creaacion de tabla de graficos de GPS
        self.fig1 = plt.figure()
        gs1 = GridSpec(1,1, figure=self.fig1)
        self.ax1 = self.fig1.add_subplot(gs1[0,0], projection='3d')
        self.canva_graf_3D = FigureCanvasTkAgg(self.fig1, master=self.white_gps_frame)
        self.canva_graf_3D.get_tk_widget().pack(expand=True, fill='both')
        #root.protocol("WM_DELETE_WINDOW", root.quit)


                                                   
        self.white_top_label    = CTkLabel(self.white_graphics_frame, 
                                    text=
                                        "Speed:                 Temperature: \n\n\n\n\n"+
                                        "Pressure:              Wind Speed:  \n\n\n\n\n"+
                                        "Altitude:              Voltage: ", 
                                    font=("Helvetica", 20),
                                    text_color=self.color_texto_negro)
        
        #seccion de creaacion de tabla de graficos de sensores
        self.fig = plt.figure(tight_layout=True)
        gs = GridSpec(3,2, figure=self.fig)
        self.ax2 = self.fig.add_subplot(gs[0,0]) #Speed
        self.ax3 = self.fig.add_subplot(gs[0,1]) #Temperature
        self.ax4 = self.fig.add_subplot(gs[1,0]) #Pressure
        self.ax5 = self.fig.add_subplot(gs[1,1]) #Wind Speed
        self.ax6 = self.fig.add_subplot(gs[2,0]) #Altitude
        self.ax7 = self.fig.add_subplot(gs[2,1]) #Voltage

        self.canva_graf = FigureCanvasTkAgg(self.fig, master=self.white_graphics_frame)
        self.canva_graf.get_tk_widget().pack(expand=True, fill='both')

        
        self.white_bottom_label = CTkLabel(self.white_data_frame, 
                                    text=
                                        "Tilt:              Roll:", 
                                    font=("Helvetica", 20),
                                    text_color=self.color_texto_negro)
        
        self.left_label.pack(pady=10)
        self.satelites_label.place(relx=0.1,rely=0.8)
        self.white_top_label.pack(pady=100)
        self.white_bottom_label.pack(pady=20)
        
        # Switches para la telemetria
        self.switch_var_telemetry   = StringVar(value="off")
        
        self.start_telemetry_switch   = CTkSwitch(self.top_center_frame, 
                                                text="Start telemetry",
                                                progress_color="#3DBA50",
                                                command=self.telemetry_on,
                                                variable=self.switch_var_telemetry, 
                                                onvalue="on",
                                                offvalue="off",
                                                font=("Helvetica", 30),
                                                text_color=self.color_texto_negro).place(relx=0.05,rely=0.35)
        
        # Command buttons
        calibrate_altitude_button = self.custom_button(self.top_right_frame, "Calibrate Altitude", self.calibrate_altitude)
        calibrate_altitude_button.place(relx=0.05,rely=0.3)

        set_time_button = self.custom_button(self.top_right_frame, "Set time", self.set_time)
        set_time_button.place(relx=0.05,rely=0.5)

        # Botón de regresar
        backbutton = self.custom_button(self.left_frame, "Return", self.pantalla_inicial)
        backbutton.place(relx=0.2,rely=0.9)

        self.configuracion_graficos()

        #self.actualizar_contenido()    

    def configuracion_graficos(self):
        # Iniciar hilo para actualizar los gráficos cada segundo
        self.thread_graficos = threading.Thread(target=self.actualizar_graficos)
        self.thread_graficos.daemon = True
        self.thread_graficos.start()

        # Iniciar hilo para actualizar el cronómetro cada segundo
        #self.label_cronometro = tk.Label(root, text="Tiempo transcurrido: 00:00:00", font=("Helvetica", 16))
        #self.label_cronometro.pack()
        self.thread_cronometro = threading.Thread(target=self.actualizar_cronometro)
        self.thread_cronometro.daemon = True
        self.thread_cronometro.start()

    def actualizar_cronometro(self):
        while True:
            tiempo_transcurrido = int(time.time() - self.inicio_tiempo)
            horas, segundos = divmod(tiempo_transcurrido, 3600)
            minutos, segundos = divmod(segundos, 60)
            tiempo_formateado = "{:02}:{:02}:{:02}".format(horas, minutos, segundos)
            #self.label_cronometro.config(text=f"Tiempo transcurrido: {tiempo_formateado}")
            time.sleep(1)
            #self.root.after(0,lambda:self.root.state('zoomed'))
        
    def actualizar_graficos(self):
        #to do: caso en que haya que deterner
        #   Agregar unidades a cadaa valor de grafico
        while True:
            try: 
                # Obtener el tiempo transcurrido en segundos
                tiempo_transcurrido = time.time() - self.inicio_tiempo

                # Llamar a los métodos individuales para cada gráfico
                self.actualizar_grafico1(tiempo_transcurrido,"GPS")#GPS
                self.actualizar_grafico2(tiempo_transcurrido,"Speed")#Speed
                self.actualizar_grafico3(tiempo_transcurrido,"Temperature")#Temperature
                self.actualizar_grafico4(tiempo_transcurrido,"Pressure")#Pressure
                self.actualizar_grafico5(tiempo_transcurrido,"Wind Speed")#Wind Speed
                self.actualizar_grafico6(tiempo_transcurrido,"Altitude")#Altitude
                self.actualizar_grafico7(tiempo_transcurrido,"Voltage")#Voltage

                # Actualizar la interfaz gráfica
                self.canva_graf.draw()
                # Actualizar la interfaz gráfica 3D
                self.canva_graf_3D.draw()

                # Esperar un segundo
                time.sleep(1)
            except:
                print("Se detuvo la carga de los graficos")
                break
            
    def actualizar_grafico1(self, tiempo_transcurrido,titulo):
        nuevo_z = random.random()

        # Agregar los nuevos datos a la lista correspondiente
        self.datos_grafico1.append((tiempo_transcurrido, nuevo_z))

        # Limitar la cantidad de puntos mostrados a, por ejemplo, 10
        if len(self.datos_grafico1) > 10:
            self.datos_grafico1 = self.datos_grafico1[-10:]

        # Limpiar y trazar el gráfico con los nuevos datos
        self.ax1.clear()
        x_data, z_data = zip(*self.datos_grafico1)
        self.ax1.plot(x_data, z_data, marker='o')
        self.ax1.set_title(titulo+'(3D)')
        self.ax1.set_xlabel('Tiempo transcurrido (segundos)')
        self.ax1.set_ylabel('Eje Z')
        self.ax1.set_zlabel(titulo)

    def actualizar_grafico2(self, tiempo_transcurrido,titulo):
        self.actualizar_grafico(self.datos_grafico2, self.ax2, 2, tiempo_transcurrido, titulo)

    def actualizar_grafico3(self, tiempo_transcurrido,titulo):
        self.actualizar_grafico(self.datos_grafico3, self.ax3, 3, tiempo_transcurrido, titulo)

    def actualizar_grafico4(self, tiempo_transcurrido,titulo):
        self.actualizar_grafico(self.datos_grafico4, self.ax4, 4, tiempo_transcurrido, titulo)

    def actualizar_grafico5(self, tiempo_transcurrido,titulo):
        self.actualizar_grafico(self.datos_grafico5, self.ax5, 5, tiempo_transcurrido, titulo)

    def actualizar_grafico6(self, tiempo_transcurrido,titulo):
        self.actualizar_grafico(self.datos_grafico6, self.ax6, 6, tiempo_transcurrido, titulo)

    def actualizar_grafico7(self, tiempo_transcurrido,titulo):
        self.actualizar_grafico(self.datos_grafico7, self.ax7, 7, tiempo_transcurrido,titulo)

    def actualizar_grafico(self, datos_grafico, ax, indice, tiempo_transcurrido, titulo):#, valor, nombre_valor):
        valor = random.random()
        nombre_valor=titulo


        # Agregar los nuevos datos a la lista correspondiente
        datos_grafico.append((tiempo_transcurrido, valor))

        # Limitar la cantidad de puntos mostrados a, por ejemplo, 10
        if len(datos_grafico) > 10:
            datos_grafico = datos_grafico[-10:]

        # Limpiar y trazar el gráfico con los nuevos datos
        ax.clear()
        x_data, y_data = zip(*datos_grafico)
        ax.plot(x_data, y_data, marker='o')
        ax.set_title(titulo)
        ax.set_xlabel('Tiempo transcurrido (segundos)')
        ax.set_ylabel(nombre_valor)

    def telemetry_on(self):
        if self.switch_var_telemetry.get() == "on":
            mensaje = "CX,ON"
            #self.ser.write(mensaje.encode())
            print(mensaje)
        elif self.switch_var_telemetry.get() == "off":
            mensaje = "CX,OFF"
            #self.ser.write(mensaje.encode())
            print(mensaje)

    def heatshield_on(self):
        if self.switch_var_heatshield.get() == "on":
            mensaje = "HS,ON"
            #self.ser.write(mensaje.encode())
            print(mensaje)
        elif self.switch_var_heatshield.get() == "off":
            mensaje = "HS,OFF"
            #self.ser.write(mensaje.encode())
            print(mensaje)
    
    def parachute_on(self):
        if self.switch_var_parachute.get() == "on":
            mensaje = "PC,ON"
            #self.ser.write(mensaje.encode())
            print(mensaje)
        elif self.switch_var_parachute.get() == "off":
            mensaje = "PC,OFF"
            #self.ser.write(mensaje.encode())
            print(mensaje)
    
    def audiobeacon_on(self):
        if self.switch_var_audiobeacon.get() == "on":
            mensaje = "BCN,ON"
            #self.ser.write(mensaje.encode())
            print(mensaje)
        elif self.switch_var_audiobeacon.get() == "off":
            mensaje = "BCN,OFF"
            #self.ser.write(mensaje.encode())
            print(mensaje)

    def simulation_on(self):
        if self.switch_var_simulation.get() == "on":
            mensaje = "SIM,ON"
            #self.ser.write(mensaje.encode())
            print(mensaje)
        elif self.switch_var_simulation.get() == "off":
            mensaje = "SIM,OFF"
            #self.ser.write(mensaje.encode())
            print(mensaje)

    def calibrate_altitude(self):
        mensaje = "CAL"
        #self.ser.write(mensaje.encode())
        print(mensaje)

    def set_time(self):
        mensaje = "ST"
        #self.ser.write(mensaje.encode())
        print(mensaje)

    def save_and_export(self):
        save_csv_file = filedialog.asksaveasfilename(initialdir=r"GroundStation",
                                                     initialfile="Flight_2075",
                                                    title="Save flight as CSV file",
                                                    filetypes=(("CSV Files", "*.csv"),))

        if save_csv_file:
            # Agregar extensión .csv si no está presente en la ruta
            if not save_csv_file.endswith(".csv"):
                save_csv_file += ".csv"
            try:
                self.df.to_csv(path_or_buf=save_csv_file, index=False)
                print(f"Archivo CSV guardado en: {save_csv_file}")
                # Puedes agregar más lógica aquí según sea necesario
            except Exception as e:
                print(f"Error al escribir el archivo CSV: {str(e)}")
        else:
            print("No se guardó ningún archivo.")

    def read_and_import(self):
        open_csv_file = filedialog.askopenfilename(initialdir=r"GroundStation",
                                                title="Open CSV simulation file",
                                                filetypes=(("CSV Files", "*.csv"),))
        if open_csv_file:
            try:
                self.df = pd.read_csv(open_csv_file)
                print(self.df)
                # Puedes agregar más lógica aquí según sea necesario
            except Exception as e:
                print(f"Error al leer el archivo CSV: {str(e)}")
        else:
            print("No se seleccionó ningún archivo.")

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
            self.Last_command = self.variables[22]
            self.Last_data = self.variables[23]
            #mission time
            #hs deployed
            #pc deployed
            #mode
            
            # ... (actualizar otras variables según sea necesario)
            #self.datos_graficox.append()
            #   GPS                 ax1
            #       z,y,z
            #   Speed               ax2
            #   Temperature         ax3
            #   Pressure            ax4
            #   Wind Speed          ax5
            #   Altitude            ax6
            #   Voltage             ax7

            

        except Exception as e:
            print(f"Error al leer desde el puerto serie: {e}")

        # Actualizar labels
        self.left_label.configure(text= 
                                    "UTC Time: "            + self.UTH_time +'\n'+
                                    "Mission time: "        + self.Mission_time+'\n'+
                                    "State: "               + self.state+'\n'+
                                    "Sent packages: "       + self.Sent_packages+'\n'+
                                    "Recieved packages: "   + self.Recieved_packages+'\n'+
                                    "Last Command: "        + self.Last_command+'\n'+
                                    "Last Data: "           + self.Last_data)
    
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
        
    def clear_screen(self):        # Limpiar la pantalla
        for widget in self.root.winfo_children():
            widget.destroy()
        root.protocol("WM_DELETE_WINDOW", root.quit)

    def custom_button(self, lugar, texto, comando):
        # Configuracion de los botones
        return CTkButton(lugar, text=texto, command=comando,
        width=250, 
        height=45, 
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