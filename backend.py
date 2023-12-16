class Backend:
    def __init__(self):
        # Inicializar datos de ejemplo
        self.datos = [("Juan", 25), ("María", 30), ("Carlos", 22)]

    def obtener_datos(self):
        # Método para obtener datos del backend
        return self.datos

    def realizar_accion(self):
        # Método para realizar acciones en el backend
        print("Se realizó una acción en el backend.")
