import tkinter as tk
from PIL import Image, ImageTk

class InterfazApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Interfaz con Tkinter y Pillow")

        # Cargar las imágenes con Pillow
        #self.img_a = self.load_image("imagen_a.png")
        #self.img_b = self.load_image("imagen_b.png")

        # Pantalla Inicial
        self.pantalla_inicial()

    def load_image(self, path):
        image = Image.open(path)
        photo = ImageTk.PhotoImage(image)
        return photo

    def pantalla_inicial(self):
        # Limpiar la pantalla actual
        self.clear_screen()

        # Configurar la pantalla inicial
        width = self.root.winfo_screenwidth()
        height = self.root.winfo_screenheight()
        self.root.geometry(f"{width}x{height}")
        self.root.configure(bg="blue")

        # Crear un Frame azul en el centro
        frame = tk.Frame(self.root, bg="red", width=300, height=200)
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        tk.Label(frame, text="Pantalla Inicial", font=("Helvetica", 16)).pack(pady=20)

        # Botones e imágenes
        tk.Button(frame, text="Ir a Pantalla A", command=self.pantalla_a).pack(pady=10)
        #tk.Label(frame, image=self.img_a).pack()

        tk.Button(frame, text="Ir a Pantalla B", command=self.pantalla_b).pack(pady=10)
        #tk.Label(frame, image=self.img_b).pack()

    def pantalla_a(self):
        # Limpiar la pantalla actual
        self.clear_screen()

        # Configurar la pantalla A
        width = self.root.winfo_screenwidth()
        height = self.root.winfo_screenheight()
        self.root.geometry(f"{width}x{height}")

        tk.Label(self.root, text="Pantalla A", font=("Helvetica", 16)).pack(pady=20)

        # Botón de regresar
        tk.Button(self.root, text="Regresar", command=self.pantalla_inicial).pack(pady=10)

    def pantalla_b(self):
        # Limpiar la pantalla actual
        self.clear_screen()

        # Configurar la pantalla B
        width = self.root.winfo_screenwidth()
        height = self.root.winfo_screenheight()
        self.root.geometry(f"{width}x{height}")

        tk.Label(self.root, text="Pantalla B", font=("Helvetica", 16)).pack(pady=20)

        # Botón de regresar
        tk.Button(self.root, text="Regresar", command=self.pantalla_inicial).pack(pady=10)

    def clear_screen(self):
        # Limpiar la pantalla
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazApp(root)
    root.mainloop()
