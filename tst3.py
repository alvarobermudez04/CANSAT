import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import pandas as pd #pip install matplotlib pandas
from pandas.plotting import register_matplotlib_converters

# Registra convertidores para fechas si es necesario
register_matplotlib_converters()

# Crear datos de ejemplo (puedes reemplazar esto con tu DataFrame)
data = {'Fecha': pd.date_range('2023-01-01', '2023-01-10'),
        'Valor': [10, 15, 20, 18, 25, 30, 22, 28, 35, 40]}
df = pd.DataFrame(data)

# Función para graficar en Matplotlib
def plot_graph():
    # Limpiar el área de la figura si ya hay un gráfico
    for widget in frame.winfo_children():
        widget.destroy()

    # Crear una figura de Matplotlib
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.plot(df['Fecha'], df['Valor'], marker='o', linestyle='-')
    ax.set_title('Gráfico de ejemplo')
    ax.set_xlabel('Fecha')
    ax.set_ylabel('Valor')

    # Integrar la figura en la interfaz de Tkinter
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack()

# Crear la ventana principal de Tkinter
root = tk.Tk()
root.title("Interfaz con Matplotlib")

# Crear un marco para colocar el gráfico
frame = ttk.Frame(root)
frame.pack(padx=10, pady=10)

# Botón para actualizar el gráfico
update_button = ttk.Button(root, text="Actualizar Gráfico", command=plot_graph)
update_button.pack(pady=10)

# Inicializar el gráfico
plot_graph()

# Iniciar el bucle principal de Tkinter
root.mainloop()
