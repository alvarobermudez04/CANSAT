from customtkinter import *

class InterfazApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GroundStation")

        self.root.configure(fg_color="white")
        self.root.after(0, lambda: self.root.state('zoomed'))

        self.frame = CTkFrame(self.root, fg_color="gray")
        self.frame.place(relwidth=0.26, relheight=1)

        self.label = CTkLabel(self.frame, text="Texto inicial")
        self.label.pack(pady=10)
        self.numero = 0

        self.start_stop_button = CTkButton(self.frame, text="Start/Stop", command=self.toggle_count)
        self.start_stop_button.pack(pady=10)

        self.counting = False
        self.actualizar_contenido()

    def toggle_count(self):
        # Cambiar el estado de la cuenta (iniciar/detener)
        self.counting = not self.counting

    def actualizar_contenido(self):
        if self.counting:
            self.numero += 1
            nuevo_texto = str(self.numero)
            self.label.configure(text=nuevo_texto)

        # Llamar a la función después de 1000 milisegundos (1 segundo)
        self.root.after(1000, self.actualizar_contenido)


if __name__ == "__main__":
    root = CTk()
    app = InterfazApp(root)
    root.mainloop()
