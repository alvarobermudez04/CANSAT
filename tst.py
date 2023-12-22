from customtkinter import *     #pip install customtkinter
from PIL import Image           #pip install PIL

class InterfazApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GroundStation")

        # Pantalla Inicial
        self.pantalla_inicial()
        
    def pantalla_inicial(self):
        # Limpiar la pantalla actual
        self.clear_screen()
        
        # Lista de colores
        self.color_fondo        = "#FAFAFA"
        self.color_frame        = "#0E1734"
        self.color_bordes       = "#636363"
        self.color_texto_blanco = "#D9D9D9"
        self.color_texto_negro  = "#1A1A1A"

        # Configura fullsize y color de fondo
        self.root.configure(fg_color=self.color_fondo)
        self.root.after(0,lambda:self.root.state('zoomed'))
        
        # Crear un Frame para el titulo y los botones en el centro
        background_frame = CTkFrame(self.root)
        background_frame.place(relwidth=1,relheight=1)
        main_frame = CTkFrame(self.root, fg_color=self.color_frame,corner_radius=30)
        main_frame.place(relx=0.55,relwidth=0.45,relheight=1)
        

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
        
        # Imagen logo
        CTkLabel(self.left_frame, image=self.team_logo, text="").pack(pady=10)

        # Titulo
        CTkLabel(self.left_frame, text="Team #2075", font=("Helvetica", 20),text_color=self.color_texto_blanco).pack(pady=20)

        # Boton simulacion
        simulationbutton = self.custom_button(self.left_frame, "Go to simulation", self.pantalla_simulation)
        simulationbutton.pack(pady=10)

        # Botón de regresar
        backbutton = self.custom_button(self.left_frame, "Return", self.pantalla_inicial)
        backbutton.pack(pady=10)

        self.center_frame = CTkFrame(self.root, fg_color=self.color_texto_blanco, border_color=self.color_bordes,border_width=4,corner_radius=20)
        self.center_frame.place(relx=0.28, rely=0.02,relwidth=0.7,relheight=0.32)
        
        # Variables
        state = "not conected"
        Sent_packages = "0"
        Recieved_packages = "0"
        Last_command = "NA"
        UTH_time = "hh:mm:ss"
        Mission_time = "T hh:mm:ss"
        HeatShield = "Not Deployed"
        Parachute = "Not Deployed"
        Satelites = "0"
        GPS_time = "hh:mm:ss"
        GPS_latitude = "x"
        GPS_longitude = "x"
        GPS_altiude = "x"
        Speed = "x"
        Pressure = "x"
        Temperature = "x"
        WindSpeed = "x"
        Altitude = "x"
        Tilt_x = "x"
        Tilt_y = "x"
        Roll = "x"
        Voltage = "x"




        self.bottom_frame = CTkFrame(self.root, fg_color=self.color_texto_blanco, border_color=self.color_bordes,border_width=4,corner_radius=20)  
        self.bottom_frame.place(relx=0.28, rely=0.37,relwidth=0.7,relheight=0.6)



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
        return CTkButton(lugar, text=texto, command=comando,width=300, height=50, corner_radius=30,fg_color="transparent",border_width=3,border_color=self.color_bordes,hover_color="#243B86")

if __name__ == "__main__":
    root = CTk()
    app = InterfazApp(root)
    root.mainloop()