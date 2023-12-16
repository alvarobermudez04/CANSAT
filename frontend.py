import tkinter as tk
from tkinter import ttk

class VentanaPrincipal(tk.Tk):
    def __init__(self, backend):
        tk.Tk.__init__(self)
        self.title("GroundStation")

        # Obtener las dimensiones de la pantalla
        ancho_pantalla = self.winfo_screenwidth()
        alto_pantalla = self.winfo_screenheight()

        # Establecer el tamaño de la ventana al tamaño de la pantalla
        self.geometry(f"{ancho_pantalla}x{alto_pantalla}")

        self.backend = backend  # Referencia al backend

        # Código de color HTML para el fondo y texto
        color_fondo_html = "#DE1600"
        color_texto_html = "#332A29"

        # Establecer el color de fondo y texto usando los códigos HTML
        self.configure(bg=color_fondo_html)

        # Crear una tabla
        self.tabla = ttk.Treeview(self, style="My.Treeview")
        self.tabla["columns"] = ("Nombre", "Edad")
        self.tabla.heading("#0", text="ID")
        self.tabla.column("#0", width=50)
        self.tabla.heading("Nombre", text="Nombre")
        self.tabla.heading("Edad", text="Edad")
        self.tabla.pack(pady=10)

        # Crear un botón
        boton = tk.Button(self, text="Obtener Datos", command=self.obtener_datos, bg=color_fondo_html, fg=color_texto_html)
        boton.pack(pady=10)

    def obtener_datos(self):
        # Llamar al método del backend para obtener datos
        datos = self.backend.obtener_datos()
        
        # Limpiar la tabla antes de agregar nuevos datos
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        # Agregar los datos a la tabla
        for i, (nombre, edad) in enumerate(datos, start=1):
            self.tabla.insert("", "end", iid=i, values=(nombre, edad))

if __name__ == "__main__":
    # Este bloque es para probar la interfaz de forma independiente
    from backend import Backend
    backend = Backend()
    ventana = VentanaPrincipal(backend)
    ventana.mainloop()
