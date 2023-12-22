import tkinter as tk
from PIL import Image, ImageTk

class InterfazApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GroundStation")

        # Pantalla Inicial
        self.pantalla_inicial()

    def pantalla_inicial(self):
        # Limpiar la pantalla actual
        self.clear_screen()

        # Configurar la pantalla inicial
        width = self.root.winfo_screenwidth()
        height = self.root.winfo_screenheight()
        self.root.geometry(f"{width}x{height}")
        self.root.configure(bg="blue")

        # Crear un Frame rojo en el centro
        frame_main = tk.Frame(self.root, bg="red")
        frame_main.pack(pady=20)

        tk.Label(frame_main, text="Team #2075", font=("Helvetica", 16)).pack(pady=20)

        # Botones e imágenes
        tk.Button(frame_main, text="New Mission", command=self.pantalla_mission).pack(pady=10)
        tk.Button(frame_main, text="Go to simulation", command=self.pantalla_simulation).pack(pady=10)

        frame_imagenes_main = tk.Frame(self.root)
        frame_imagenes_main.pack(pady=10)


        # Cargar las imágenes
        self.gia_logo = ImageTk.PhotoImage(Image.open("GroundStation\gia logo.jpg").resize((200,200)))
        self.cansat_logo = ImageTk.PhotoImage(Image.open("GroundStation\cansat logo.png").resize((200,200)))
        self.team_logo = ImageTk.PhotoImage(Image.open("GroundStation\\team logo.jpg").resize((200,200)))

        #coloca las imagenes en el frame2
        tk.Label(frame_imagenes_main, image=self.gia_logo).pack(side="left")
        tk.Label(frame_imagenes_main, image=self.cansat_logo).pack(padx=10,side="left")
        tk.Label(frame_imagenes_main, image=self.team_logo).pack()

    def pantalla_mission(self):
        # Limpiar la pantalla actual
        self.clear_screen()

        # Configurar la pantalla A
        width = self.root.winfo_screenwidth()
        height = self.root.winfo_screenheight()
        self.root.geometry(f"{width}x{height}")

        tk.Label(self.root, text="Mission", font=("Helvetica", 16)).pack(pady=20)

        # Botón de regresar
        tk.Button(self.root, text="Return", command=self.pantalla_inicial).pack(pady=10)

    def pantalla_simulation(self):
        # Limpiar la pantalla actual
        self.clear_screen()

        # Configurar la pantalla B
        width = self.root.winfo_screenwidth()
        height = self.root.winfo_screenheight()
        self.root.geometry(f"{width}x{height}")

        tk.Label(self.root, text="Simulation Mode", font=("Helvetica", 16)).pack(pady=20)

        # Botón de regresar
        tk.Button(self.root, text="Return", command=self.pantalla_inicial).pack(pady=10)

    def clear_screen(self):
        # Limpiar la pantalla
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazApp(root)
    root.mainloop()
