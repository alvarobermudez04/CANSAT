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

        self.color_fondo        = "#FAFAFA"
        self.color_frame        = "#0E1734"
        self.color_bordes       = "#636363"
        self.color_texto_blanco = "#D9D9D9"
        self.color_texto_negro  = "#1A1A1A"

        # Configura fullsize y color de fondo
        self.root.configure(fg_color=self.color_fondo)
        self.root.after(0,lambda:self.root.state('zoomed'))
        
        # Crear un Frame para el titulo y los botones en el centro
        main_frame = CTkFrame(self.root, fg_color=self.color_frame,corner_radius=30)
        main_frame.place(relx=0.55,relwidth=0.45,relheight=1)

        # Titulo
        CTkLabel(main_frame, text="Team #2075", font=("Helvetica", 16),text_color=self.color_texto_blanco).pack(pady=200)

        # Botones e imágenes
        button_mission = CTkButton(main_frame, text="New Mission", command=self.pantalla_mission, width=300,height=50,corner_radius=30,border_width=3).pack(pady=10)
        
        button_simulation = CTkButton(main_frame, text="Go to simulation", command=self.pantalla_simulation,width=300,height=50,corner_radius=30,border_width=3).pack(pady=10)
        
        img_size=150
        # Cargar las imágenes
        self.gia_logo = CTkImage(dark_image=Image.open("GroundStation\gia logo.jpg"), size=(img_size,img_size))
        self.cansat_logo = CTkImage(dark_image=Image.open("GroundStation\cansat logo.png"), size=(img_size,img_size))
        self.team_logo = CTkImage(dark_image=Image.open("GroundStation\\team logo.jpg"), size=(img_size,img_size))

        #coloca las imagenes
        CTkLabel(main_frame, image=self.team_logo, text="").place(rely=0.7,relx=0.375*2-0.02)
        CTkLabel(main_frame, image=self.gia_logo, text="").place(rely=0.7,relx=0.02)
        CTkLabel(main_frame, image=self.cansat_logo, text="").place(rely=0.7,relx=0.375)
        
        
    def pantalla_mission(self):
        # Limpiar la pantalla actual
        self.clear_screen()

        # Frames
        self.left_frame = CTkFrame(self.root, fg_color=self.color_frame)
        self.left_frame.place(relwidth=0.26,relheight=1)
        
        self.center_frame = CTkFrame(self.root, fg_color=self.color_texto_blanco, border_color=self.color_bordes,border_width=4,corner_radius=20)
        self.center_frame.place(relx=0.28, rely=0.02,relwidth=0.7,relheight=0.32)

        self.bottom_frame = CTkFrame(self.root, fg_color=self.color_texto_blanco, border_color=self.color_bordes,border_width=4,corner_radius=20)  
        self.bottom_frame.place(relx=0.28, rely=0.37,relwidth=0.7,relheight=0.6)
        
        # Imagen logo
        CTkLabel(self.left_frame, image=self.team_logo, text="").pack(pady=10)

        # Titulo
        CTkLabel(self.left_frame, text="Team #2075", font=("Helvetica", 16)).pack(pady=20)

        # Boton simulacion
        simulationbutton = self.custom_button(self.left_frame, "Go to simulation", self.pantalla_simulation)
        simulationbutton.pack(pady=10)

        # Botón de regresar
        backbutton = self.custom_button(self.left_frame, "Return", self.pantalla_inicial)
        backbutton.pack(pady=10)

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
        return CTkButton(lugar, text=texto, command=comando, width=300, height=50, corner_radius=30)

if __name__ == "__main__":
    root = CTk()
    app = InterfazApp(root)
    root.mainloop()
